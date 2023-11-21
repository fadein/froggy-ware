import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from engine.conversions import ms_to_min
import configuration.password_info

class SpotifyEngine:
	def __init__(self, playlist_url):
		cid = configuration.password_info.get_cid()
		secret = configuration.password_info.get_secret()
		client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
		self.sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
		self.playlist = playlist_url
	
	def get_playlists(self, verbose = False):
		playlist_link = self.playlist
		playlist_URI = playlist_link.split("/")[-1].split("?")[0]
		track_uris = [x["track"]["uri"] for x in self.sp.playlist_tracks(playlist_URI)["items"]]


		songs = []
		for track in self.sp.playlist_tracks(playlist_URI)["items"]:

			songInfo = {}
    
			#Track name
			track_name = track["track"]["name"]
    
			#Name, popularity, genre
			artist_name = track["track"]["artists"][0]["name"]
    
			#Album
			album = track["track"]["album"]["name"]

			#length milliseconds
			ms_duration = track['track']['duration_ms']

			#length formatted
			formatted_duration = ms_to_min(int(ms_duration))
	
			songInfo['track'] = track_name
			songInfo['artist'] = artist_name
			songInfo['album'] = album
			songInfo['duration_ms'] = ms_duration
			songInfo['duration_formatted'] = formatted_duration

			if verbose:
				album_href = track['track']['album']['images'][0]['url']
				release_date = track['track']['album']['release_date']
				track_number = track['track']['track_number']
			
				songInfo['album_art'] = album_href
				songInfo['release_date'] = release_date
				songInfo['track_number'] = track_number

			songs.append(songInfo)
	
		return songs

	def get_album(self, verbose = False):
		content_link = self.playlist
		content_URI = content_link.split("/")[-1].split("?")[0]
		songs = []

		album_info = self.sp.album(content_URI, "US")
		
		album_name = album_info['name']

		for track in self.sp.album_tracks(content_URI)["items"]:

			songInfo = {}

			#Track name
			track_name = track["name"]

			#Name, popularity, genre
			artist_name = track["artists"][0]["name"]

			#length millisecond
			ms_duration = track['duration_ms']

			#length formatted
			formatted_duration = ms_to_min(int(ms_duration))

			songInfo['track'] = track_name
			songInfo['artist'] = artist_name
			songInfo['album'] = album_name
			songInfo['duration_ms'] = ms_duration
			songInfo['duration_formatted'] = formatted_duration

			if verbose:
				album_href = album_info['images'][0]['url']
				release_date = album_info['release_date']
				track_number = track['track_number']

				songInfo['album_art'] = album_href
				songInfo['release_date'] = release_date
				songInfo['track_number'] = track_number

			songs.append(songInfo)
		
		return songs

	
	def set_playlist(self, url):
		self.playlist = url
	
	def get_playlist_url(self):
		return self.playlist

	def get_playlist_name(self):
		results = spotipy.user_playlist(user=None, playlist_id="3cqDkXVInhOYPpJyVzvwux", fields="name")
		return(results["name"])


if __name__ == "__main__":
	playlist = input("PLAYLIST URL\n:")
	engine = SpotifyEngine(playlist)
	songs = engine.get_playlists_verbose()
	
	for key in (songs[0])['track']:
#		print(f"{key} -> {(songs[0])[key]}")
		print(key)
		print("-------------------")
		print(f"{((((songs[0])['track'])['duration_ms']))} MS")
		print(f"{((((songs[0])['track'])['duration_ms'])/60000)} MINUTES")
		print("-------------------")
	    
