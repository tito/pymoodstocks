from pymoodstocks import MoodstocksBase
from pyobjus import autoclass, protocol
from pyobjus.protocols import protocols

protocols["MSAutoScannerSessionDelegate"] = {
    'session:didFindResult:': ('v16@0:4@8@12', 'v32@0:8@16@24'),
    'session:didFindResult:forVideoFrame:': ('v20@0:4@8@12@16', 'v40@0:8@16@24@32'),
    'session:didEncounterWarning:': ('v16@0:4@8@12', 'v32@0:8@16@24')}
protocols["MSManualScannerSessionDelegate"] = {
    'sessionWillStartServerRequest:': ('v12@0:4@8', 'v24@0:8@16'),
    'session:didFindResult:optionalQuery:': ('v20@0:4@8@12@16', 'v40@0:8@16@24@32'),
    'session:didFailWithError:': ('v16@0:4@8@12', 'v32@0:8@16@24'),
    'session:didEncounterWarning:': ('v16@0:4@8@12', 'v32@0:8@16@24')}
protocols["PyMSScannerDelegate"] = {
    'buttonClicked': ('v8@0:4', 'v16@0:8')}

MSResultTypeNone = 0
MSResultTypeEAN8 = 1 << 0
MSResultTypeEAN13 = 1 << 1
MSResultTypeQRCode = 1 << 2
MSResultTypeDatamatrix = 1 << 3
MSResultTypeImage = 1 << 31


class Moodstocks(MoodstocksBase):

    def init(self):
        self.scanner = autoclass("PyMSScanner").alloc().initWithApiKey_secret_delegate_(
                self.api_key, self.api_secret, self)
        self.scanner.setTitle_(self.title)

    def start(self):
        self.scanner.setPopup(int(self.popup))
        self.scanner.start()

    def stop(self):
        self.scanner.stop()

    def resume(self):
        self.scanner.resume()

    @protocol("PyMSScannerDelegate")
    def buttonClicked(self):
        self.dispatch("on_button_clicked")

    @protocol("MSAutoScannerSessionDelegate")
    def session_didFindResult_(self, session, result):
        result_type_i = result.type
        if result_type_i == MSResultTypeNone:
            self.result_type = "none"
        elif result_type_i == MSResultTypeEAN8:
            self.result_type = "ean8"
        elif result_type_i == MSResultTypeEAN13:
            self.result_type = "ean13"
        elif result_type_i == MSResultTypeQRCode:
            self.result_type = "qrcode"
        elif result_type_i == MSResultTypeDatamatrix:
            self.result_type = "datamatrix"
        else:
            self.result_type = "image"
        self.result_data = result.string.UTF8String()
        self.dispatch("on_scan", self.result_type, self.result_data)

