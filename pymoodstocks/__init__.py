"""
Moodstocks Python wrapper
=========================

"""

__all__ = ("Moodstocks", )

from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import StringProperty


class MoodstocksBase(EventDispatcher):

    __events__ = ("on_button_clicked", "on_scan")

    title = StringProperty("Scan an object")
    result_data = StringProperty(allownone=True)
    result_type = StringProperty(allownone=True)

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

    def on_button_clicked(self):
        self.stop()

    def on_scan(self, result_type, result_data):
        pass


if platform == "ios":
    from pymoodstocks.ios import Moodstocks
else:
    raise Exception("Unsupported platform")
