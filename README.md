# Moodstocks Python wrapper

This wrapper allow you to use the Moodstock iOS and Android SDK with Kivy /
Python. This current version include an UI for both iOS and Android, and do all
the effort to display it correctly. The default configuration searchs for
qrcode, barcode and image.

![Scanner in action](https://cloud.githubusercontent.com/assets/37904/6444358/6661b88a-c0fd-11e4-8bc9-ed1d4de44f82.png)
![Scanner result](https://cloud.githubusercontent.com/assets/37904/6444362/6b3603fc-c0fd-11e4-93e3-f48c9f2addbb.png)

## Installation

### iOS

You need to use the latest kivy-ios toolchain (on the branch poly-arch):

    ./toolchain.py build pymoodstocks

Then either create or update an Xcode project with the toolchain. It will add
the frameworks necessary for Moodstocks and libraries for pymoodstocks.

### Android

With buildozer, you need to download the SDK for eclipse, and extract the libs/
directory into a directory named sdk (for example). Then changes in the
buildozer.spec:

	[app]
	source.exclude_dirs = sdk
	android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE
	android.add_libs_armeabi = sdk/libs/armeabi/*.so
	android.add_libs_armeabi_v7a = sdk/libs/armeabi-v7a/*.so
	android.add_libs_x86 = sdk/libs/x86/*.so
	android.add_libs_mips = sdk/libs/mips/*.so

Then (currently), you need to copy the pymoodstocks directory into your app.


## Usage

Create a Moodstocks instance and pass your Moodstocks API key/secret:

	from pymoodstocks import Moodstocks
	moodstocks = Moodstocks(KEY, SECRET)

Then, you can bind a method to get the scan result on the fly:

	def on_scan(self, result_type, result_data):
		print("I got something of type {}: {}".format(
			  result_type, result_data))
		moodstocks.stop()

	def on_button_clicked(self, result_type, result_data):
		print("Button DONE click, stop the scanner")
		moodstocks.stop()

	moodstocks.bind(on_scan=self.on_scan,
					on_button_clicked=self.on_button_clicked)

At any time, you can start the scanner:

	moodstocks.start()

The scanner will stop processing after it detect something / on_scan method is
called. You could resume the scanner instead of closing it by calling:

	moodstocks.resume()


## Todo

- Let the user choose which type to search for
- Implement synchronisation callback on iOS

