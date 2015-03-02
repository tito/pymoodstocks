from android.runnable import run_on_ui_thread
from pymoodstocks import MoodstocksBase
from jnius import autoclass, PythonJavaClass, java_method, cast
from kivy.clock import Clock
from kivy.metrics import sp
from threading import Lock
from collections import deque


Scanner = autoclass("com.moodstocks.android.Scanner")
AutoScannerSession = autoclass("com.moodstocks.android.AutoScannerSession")
Result = autoclass("com.moodstocks.android.Result")
ResultType = autoclass("com.moodstocks.android.Result$Type")
PythonActivity = autoclass("org.renpy.android.PythonActivity")
RelativeLayout = autoclass("android.widget.RelativeLayout")
LayoutParams = autoclass("android.widget.RelativeLayout$LayoutParams")
SurfaceView = autoclass("android.view.SurfaceView")
Gravity = autoclass("android.view.Gravity")
String = autoclass("java.lang.String")
context = PythonActivity.mActivity

TYPES = ResultType.IMAGE | ResultType.QRCODE | ResultType.EAN13


class ClickListener(PythonJavaClass):
    __javainterfaces__ = ["android.view.View$OnClickListener"]

    def __init__(self, scanner):
        super(ClickListener, self).__init__()
        self.scanner = scanner

    @java_method("(Landroid/view/View;)V")
    def onClick(self, view):
        self.scanner.safe_dispatch("on_button_clicked")


class SyncListener(PythonJavaClass):
    __javainterfaces__ = ["com.moodstocks.android.Scanner$SyncListener"]
    __javacontext__ = "app"

    def __init__(self, scanner):
        super(SyncListener, self).__init__()
        self.scanner = scanner

    @java_method("()V")
    def onSyncStart(self):
        self.scanner.safe_dispatch("on_sync_start")

    @java_method("()V")
    def onSyncComplete(self):
        self.scanner.safe_dispatch("on_sync_complete")

    @java_method("(Lcom/moodstocks/android/MoodstocksError;)V")
    def onSyncFailed(self, error):
        self.scanner.safe_dispatch("on_sync_failed",
                              error.getErrorCode(),
                              error.getMessage())

    @java_method("(II)V")
    def onSyncProgress(self, total, current):
        self.scanner.safe_dispatch("on_sync_start", total, current)


class AutoScannerSessionListener(PythonJavaClass):
    __javainterfaces__ = ["com.moodstocks.android.AutoScannerSession$Listener"]
    __javacontext__ = "app"

    def __init__(self, scanner):
        super(AutoScannerSessionListener, self).__init__()
        self.scanner = scanner

    @java_method("(Ljava/lang/Exception;)V")
    def onCameraOpenFailed(self, e):
        pass

    @java_method("(Lcom/moodstocks/android/Result;)V")
    def onResult(self, result):
        result_type_i = result.getType()
        if result_type_i == ResultType.NONE:
            result_type = "none"
        elif result_type_i == ResultType.EAN8:
            result_type = "ean8"
        elif result_type_i == ResultType.EAN13:
            result_type = "ean13"
        elif result_type_i == ResultType.QRCODE:
            result_type = "qrcode"
        elif result_type_i == ResultType.DATAMATRIX:
            result_type = "datamatrix"
        else:
            result_type = "image"
        result_data = result.getValue()
        self.scanner.safe_dispatch("on_scan", result_type, result_data)

    @java_method("(Ljava/lang/String;)V")
    def onWarning(self, warning):
        print("MoodstocksWarning: {}".format(warning))


class Moodstocks(MoodstocksBase):

    def init(self):
        self._preview = None
        self._queue = deque()
        self._lock = Lock()
        self._trigger = Clock.create_trigger(self._dispatch_queue)
        self._sync = SyncListener(self)
        self._listener = AutoScannerSessionListener(self)
        self._click = ClickListener(self)
        self._session = None
        self.scanner = None
        if not Scanner.isCompatible():
            raise Exception("Incompatible camera for the Scanner")

        try:
            self.scanner = Scanner.get()
            db = Scanner.pathFromFilesDir(context, "scanner.db")
            self.scanner.open(db, self.api_key, self.api_secret)
            run_on_ui_thread(self.scanner.sync)()
        except:
            raise Exception("MoodstocksError")

    def unload(self):
        if not self.scanner:
            return
        self.stop()
        self.scanner.close()
        self.scanner.destroy()
        self.scanner = None

    @run_on_ui_thread
    def start(self):
        # create a surface for displaying the preview

        # XXX android issue or moodstocks issue, i don't known
        # but if we don't recreate the preview and session,
        # the recognition works only one time.
        self._preview = None
        self._session = None

        preview = self._create_preview()
        if not self._session:
            self._session = AutoScannerSession(
                    context,
                    self.scanner,
                    self._listener,
                    preview)
            self._session.setResultTypes(TYPES)
        self._session.start()

    @run_on_ui_thread
    def stop(self):
        self._session.stop()
        context.setContentView(PythonActivity.mView)

    @run_on_ui_thread
    def resume(self):
        self._session.resume()

    def _create_preview(self):
        # -1 = MATCH_PARENT
        if not self._preview:
            self._preview_rlp = LayoutParams(-1, -1)
            layout = RelativeLayout(context)
            view = SurfaceView(context)
            view.setLayoutParams(self._preview_rlp)
            layout.addView(view)
            self._preview_layout = layout
            self._preview = view

            # create a toolbar
            TextView = autoclass("android.widget.TextView")
            Button = autoclass("android.widget.Button")
            toolbar = RelativeLayout(context)
            toolbar.setBackgroundColor(0xff4384f6 % (2 ** 31 - 1))
            toolbar.setVerticalGravity(RelativeLayout.CENTER_VERTICAL)
            x = sp(2)
            h = sp(48)
            toolbar.setPaddingRelative(x, x, x, x)
            toolbar.setLayoutParams(LayoutParams(-1, h))
            layout.addView(toolbar)
            text = TextView(context)
            button = Button(context)
            button.setOnClickListener(self._click)
            toolbar.addView(text)
            toolbar.addView(button)

            lp = LayoutParams(-1, h)
            lp.addRule(RelativeLayout.ALIGN_PARENT_LEFT)
            lp.addRule(RelativeLayout.CENTER_IN_PARENT)
            text.setLayoutParams(lp)
            text.setGravity(Gravity.CENTER)
            lp = LayoutParams(-2, h)
            lp.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
            lp.addRule(RelativeLayout.CENTER_IN_PARENT)
            button.setLayoutParams(lp)
            button.setPaddingRelative(sp(20), 0, sp(20), 0)

            sb = String("Done")
            button.setText(cast("java.lang.CharSequence", sb))
            self._preview_title = text
            self._set_title(self.title)

        context.setContentView(self._preview_layout, self._preview_rlp)
        return self._preview

    def _set_title(self, title):
        self._preview_title.setText(
            cast("java.lang.CharSequence", String(self.title)))

    def on_title(self, instance, value):
        self._set_title(self.title)

    def safe_dispatch(self, *args):
        try:
            self._lock.acquire()
            self._queue.appendleft(args)
            self._trigger()
        finally:
            self._lock.release()

    def _dispatch_queue(self, *args):
        try:
            self._lock.acquire()
            while self._queue:
                data = self._queue.pop()
                event = data[0]
                if event == "on_scan":
                    self.result_type = data[1]
                    self.result_data = data[2]
                self.dispatch(*data)
        finally:
            self._lock.release()

