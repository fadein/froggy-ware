from pydub import AudioSegment
import eyed3
import subprocess
import os
from requests import get

# _______________________________________________________________
# |                      FILE OVERVIEW                           |
# |--------------------------------------------------------------|
# | This "Scrubber.py" file exists to add different metadata to  |
# | files. This includes tags, album arts, etc.                  |
# | The file also holds the function responsible for adjusting   |
# | all aspects of already downloaded files, such as running     |
# | FFMPEG files to clean the files                              |
# |______________________________________________________________|



def m4a_to_mp3(file_name):
	""" This function is responsible for runing the FFMPEG code that
        converts and mp4 file to 
        an mp3 file"""

	m4a_file = AudioSegment.from_file(file_name, format="m4a")
		
	m4a_file.export(f"{file_name[:-4]}.mp3", format="mp3")

def add_metadata(file_name, artist, title, album = None, track_number = None, release_date = None ):
	""" The "add_metadata" function is responsible for adding a slew 
	of metadata for an inputted mp3 file. The function takes in two
	required parameters, artist and title. There are then a series of
	optional paramters, including 
	album, track_number, and release date"""


	mp3_file = eyed3.load(file_name)
	mp3_file.tag.artist = artist
	mp3_file.tag.title = title

	if (album is not None):
		mp3_file.tag.album = album

	if (track_number is not None):
		mp3_file.tag.track_num = track_number

	
	if (release_date is not None):
		mp3_file.tag.recording_date = (release_date.split("_"))[-1]

	mp3_file.tag.save()

def add_cover_art(file_name, img_url):
	""" The "add_cover_art" function attaches the cover metadata tag to a file. 
	The function takes in a url form the internet, saves it as an image, attaches
	that image to the mp3 file, then deletes the image file"""	
	file = eyed3.load(file_name)

	img_data = get(img_url).content
	with open('temp_image.jpeg', 'wb') as handler:
		handler.write(img_data)


	with open("temp_image.jpeg", "rb") as cover_art:
		file.tag.images.set(3, cover_art.read(), "image/jpeg")

	file.tag.save(version=eyed3.id3.ID3_V2_3)

	os.remove("temp_image.jpeg")

def fix_file(file_name, directory, silence_log = True):
	"""by default, some files converted to mp3 with FFMPEG come with some 
	errors that causes integration issues with DAWs and other programs. This
	function provides as an intermediary to run the CMD commands to scrub
	and fix the data. To find the file the file name and directory must be
	specified. FFMPEG functions by default print a lot of information to the screen,
	the silence_log parameter hides this from the terminal log"""

	if silence_log:
		subprocess.run(["ffmpeg","-loglevel","quiet", "-i", file_name, "-acodec", "copy", f"{directory}/file_fixed.mp3"])
	else:
		subprocess.run(["ffmpeg","-i", file_name, "-acodec", "copy", f"{directory}/file_fixed.mp3"])

	os.remove(file_name)
	os.rename(f"{directory}/file_fixed.mp3", file_name),
