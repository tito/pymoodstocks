from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from pymoodstocks import Moodstocks

MS_API_KEY    = "XXXXXXXXXXXXXXXXX"
MS_API_SECRET = "XXXXXXXXXXXXXXXXX"


class Moodstock(App):

    moodtype = StringProperty()
    mooddata = StringProperty()

    def build(self):
        self.sound = SoundLoader.load("beep.wav")
        self.moodstocks = Moodstocks(MS_API_KEY, MS_API_SECRET)
        self.moodstocks.bind(
            on_scan=self.on_ms_scan,
            on_button_clicked=self.on_ms_clicked)
        return super(Moodstock, self).build()

    def on_ms_scan(self, *args):
        self.mooddata = self.moodstocks.result_data
        self.moodtype = self.moodstocks.result_type
        self.sound.play()
        self.moodstocks.stop()

    def on_ms_clicked(self, *args):
        self.moodstocks.stop()

    def do_scan(self):
        self.moodstocks.start()

Moodstock().run()
