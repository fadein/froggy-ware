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

	def convert_by_album(self, url):

		# This method instatiates a FroggyEngine object with the parameter "is_album" set to false.
		# Convert_by_playlist and Convert_by_album are separate methods in order to provide more helpful
		# error codes for the user, and to help with code readability

		desktop_path = os.path.expanduser("~/Desktop")
		directory = ""+desktop_path+"/NewPlaylist"

		engine = FroggyEngine(url, directory, True, True, True, True, True)
		try:
			songs = engine.get_songs()
			
			for song in songs:
				album_art = f'"{song["album_art"]}"'
				window.evaluate_js(f'document.getElementById("converting-album-art").src = {album_art}')
				window.evaluate_js(f'document.getElementById("song-name").innerText = "{song["track"]}"')
				window.evaluate_js(f'document.getElementById("artist-name").innerText = "{song["artist"]}"')	

				engine.process_single_song(song)

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')
		except Exception as e:
			print(e)
			window.evaluate_js('document.getElementById("url-input-error").innerText = "Something went wrong, try removing the failed song from your playlist"')

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')
			
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')
	
	def convert_by_playlist(self, url):

		# This method instatiates a FroggyEngine object with the parameter "is_album" set to false.
		# Convert_by_playlist and Convert_by_album are separate methods in order to provide more helpful
		# error codes for the user, and to help with code readability

		desktop_path = os.path.expanduser("~/Desktop")
		directory = ""+desktop_path+"/NewPlaylist"

		engine = FroggyEngine(url,directory, True, True, True, False, True)
		try:
			songs = engine.get_songs()

			for song in songs:
				album_art = f'"{song["album_art"]}"'
				window.evaluate_js(f'document.getElementById("converting-album-art").src = {album_art}')
				window.evaluate_js(f'document.getElementById("song-name").innerText = "{song["track"]}"')
				window.evaluate_js(f'document.getElementById("artist-name").innerText = "{song["artist"]}"')

				engine.process_single_song(song)

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')
		except Exception as e:
			window.evaluate_js('document.getElementById("url-input-error").innerText = "Something went wrong, is your playlist public?"')

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')

			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')



	def convert(self):
		url_input_box = window.evaluate_js('document.getElementById("url_input_box").value')
		if url_input_box == "":
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')
			window.evaluate_js('document.getElementById("url-input-error").innerText = "You Must Provide a Spotify Link"')


			
		else:
			window.evaluate_js('document.getElementById("url-input-error").style.visibility = "hidden"')

			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "visible"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "visible"')

		
			radio_val = window.evaluate_js("""document.querySelector('input[name="radio"]:checked').value""")

			if radio_val == "playlist":
				self.convert_by_playlist(url_input_box)

			elif radio_val == "album":
				self.convert_by_album(url_input_box)
			else:
				window.evaluate_js('document.getElementById("url-input-error").style.visibility = "visible"')
				window.evaluate_js('document.getElementById("url-input-error").innerText = "Choose an album or playlist button"')


			window.evaluate_js('document.getElementById("converting-popup").style.visibility = "hidden"')
			window.evaluate_js('document.getElementById("tint-overlay").style.visibility = "hidden"')				


 
if __name__ == '__main__':

	with open("view/index.html", "r") as f:
		html = f.read()

	api = Api()
	window = webview.create_window('Froggy Ware', html=html, js_api=api, width=1500, height=1000)
	webview.start()
