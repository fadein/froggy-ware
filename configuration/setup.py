import subprocess
import sys

# Note: WebKit2 API version 4.0 is required for the webview package on Linux
# pkg-config files: webkit2gtk-4.1
packages = [ "dearpygui", "spotipy", "pytube", "youtube-search-python", "eyed3", "pydub", "webview"]



def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
	for package in packages:
		try:
			install(package)
		except:
			print("error installing {}".format(package))

	subprocess.run(["brew", "install", "ffmpeg"])
