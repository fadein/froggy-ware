import subprocess
import sys

packages = [ "dearpygui", "spotipy", "pytube", "youtube-search-python", "eyed3", "pydub"]



def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
	for package in packages:
		try:
			install(package)
		except:
			print("error installing {}".format(package))

	subprocess.run(["brew", "install", "ffmpeg"])
