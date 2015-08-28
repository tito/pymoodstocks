"""
Moodstocks Python wrapper
=========================

"""

__all__ = ("Moodstocks", )

from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty


class MoodstocksBase(EventDispatcher):

    __events__ = (
        "on_button_clicked",
        "on_scan",
        "on_sync_start",
        "on_sync_complete",
        "on_sync_failed",
        "on_sync_progress")

    title = StringProperty("Scan an object")
    result_data = StringProperty(allownone=True)
    result_type = StringProperty(allownone=True)
    popup = BooleanProperty(True)

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        super(MoodstocksBase, self).__init__()
        self.init()

    def init(self):
        pass

    def start(self):
        """Start the moodstock scanner
        """
        pass

    def stop(self):
        """Close the view and stop the scanner
        """
        pass

    def resume(self):
        """Resume the scanner.

        This must be called if you want to check for another result after a
        result have been found.
        """
        pass

    def unload(self):
        """Unload everything we allocated.
        The scanner will not be usable after that.
        """
        pass

    def on_button_clicked(self):
        self.stop()

    def on_scan(self, result_type, result_data):
        pass

    def on_sync_start(self):
        print("Moodstocks SDK: Sync will start.")

    def on_sync_complete(self):
        print("Moodstocks SDK: Sync succeeded.")

    def on_sync_failed(self, code, message):
        print("Moodstocks SDK: Sync failed: ({}){}".format(
              code, message))

    def on_sync_progress(self, total, current):
        print("Moodstocks SDK: Sync progressing: {}%".format(
              int(float(current) / float(total) * 100)))


if platform == "ios":
    from pymoodstocks.pms_ios import Moodstocks
elif platform == "android":
    from pymoodstocks.pms_android import Moodstocks
else:
    raise Exception("Unsupported platform")
