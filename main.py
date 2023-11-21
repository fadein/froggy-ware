import random
import sys
import threading
import time
from engine.froggy_engine import FroggyEngine
import webview
import os
class Api:
	def __init__(self):
		self.cancel_heavy_stuff_flag = False

	def remove_url_warning(self):
		window.evaluate_js('document.getElementById("url-input-error").style.visibility = "hidden"')

	def convert_by_album(self):

		url_input_box = window.evaluate_js('document.getElementById("url_input_box").value')

		desktop_path = os.path.expanduser("~/Desktop")
		directory = ""+desktop_path+"/NewPlaylist"
		engine = FroggyEngine(url_input_box, directory, True, True, True, True, True )

		try:
			songs = engine.get_songs_by_album()
			
			for song in songs:
				album_art = f'"{songs[0]["album_art"]}"'
				window.evaluate_js(f'document.getElementById("converting-album-art").src = {album_art}')
				window.evaluate_js(f'document.getElementById("song-name").innerText = "{song["track"]}"')
				window.evaluate_js(f'document.getElementById("artist-name").innerText = "{song["artist"]}"')	

				engine.process_single_song(song)

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')
			
		except:
			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')
			
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')
	
	def convert(self):
		url_input_box = window.evaluate_js('document.getElementById("url_input_box").value')
		if url_input_box == "":
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')
		else:
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "hidden"')

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "visible"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "visible"')

			
			self.convert_by_album()

			#engine.process_single_song(songs[0])
			time.sleep(10)	

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')				


 
if __name__ == '__main__':

	with open("view/index.html", "r") as f:
		html = f.read()

	api = Api()
	window = webview.create_window('Froggy Ware', html=html, js_api=api, width=1500, height=1000)
	webview.start()
