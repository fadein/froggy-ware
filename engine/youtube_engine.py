from pytube import YouTube 
import os 
from youtubesearchpython import VideosSearch
from engine.conversions import minutes_to_ms
import engine.scrubber as scrubber

class YoutubeEngine:
	def __init__(self, log_bool = False):
		self.logging = log_bool

	def within_bounds(self,ms_1, ms_2, allowance):
		""" this function checks to see whether two time stamps are within 10 seconds of eachother """

		difference = abs(ms_1 - ms_2)
		if difference < (allowance * 1000):
			return True
		else:
			return False

	def search_from_list(self, songs):
		song_info = []
		for song in songs:
			#assuming list of songs is passed in from spotify_engine
			artist = song['artist']
			track = song['track']
			track_length = song['duration_ms']


			searchString = "{} {} ".format(track,artist)	
			videosSearch = VideosSearch(searchString, limit = 3)
			title = ((((videosSearch.result())['result'])[0])['title']).lower()

			if self.logging:
				print("\n----------------------------------")
				print(f"attempting to convert {title}")

			duration = (videosSearch.result())['result'][0]['duration']
			video_length = minutes_to_ms(duration)

			#check to see if video is in title, trying to filter out music videos
			
			if ("video" not in title) and (self.within_bounds(track_length, video_length, 3)):

				if self.logging:
					print(f"No issues with first link, converting {title}")

				link = (((videosSearch.result())['result'])[0])['link']

			else:
				alternate_song = (((videosSearch.result())['result'])[1])['title'].lower()
				alternate_length =  minutes_to_ms((((videosSearch.result())['result'])[1])['duration'])

				# check to see if music video is within bounds
				
				if (self.within_bounds(track_length, video_length, 6)):
					if self.logging:
						print(f"While this may be a music video, the runtime was the same. Converting {title}")
					link = (((videosSearch.result())['result'])[0])['link']

				elif (self.within_bounds(track_length, alternate_length, 1)):
					if self.logging:
						print(f"The second option was near indistinguishable in length, converting {alternate_song}")
					link = (((videosSearch.result())['result'])[1])['link']


				elif (track.lower() in alternate_song) and (self.within_bounds(track_length, alternate_length, 3)):

					#check to see if the song name itself has video in the name
					if "video" not in track.lower():
						#music video filtered, take second youtube results
												
						if self.logging:
							print(f"{title} was a music video, using {alternate_song} instead")
					
						link = (((videosSearch.result())['result'])[1])['link']		

					elif "music video" not in title:
						#"video" included in song name, check to see if it is also a youtube videoo
						link = (((videosSearch.result())['result'])[0])['link']

					else:
						#video is included in track name, and first result is a music video. Filter

						if self.logging:
							print(f"{title} was a music video, using {alternate_song} instead")
						link = (((videosSearch.result())['result'])[1])['link']

				else:
					if self.logging:
						print(f"We're having trouble converting, attempting lyrics search")

					searchString = "{} {} {}".format(track,artist,"lyrics")
					lyrics_search  = VideosSearch(searchString, limit = 3)

					for i in range(3):
						alternate_song = (((lyrics_search.result())['result'])[i])['title'].lower()
						alternate_length =  minutes_to_ms((((lyrics_search.result())['result'])[i])['duration'])

						if self.within_bounds(alternate_length, track_length, 2):
							if self.logging:
								print(f"Lyrics search was a match, converting {alternate_song}")

							link = (((lyrics_search.result())['result'])[0])['link']
							break
						else:
							if i == 2:
								if self.logging:
									print(f"All attempts to reconcile issue failed, taking chances and converting {title}")
									link = (((videosSearch.result())['result'])[0])['link']
							continue
					
			track = {'link':link}
			for key in song:
				track[key] = song[key]

			song_info.append(track)
			
		return song_info

			

	def download_track(self, url, artist, track, directory, sam_configuration = False, total_data = None):
		yt = YouTube(url,use_oauth=True,allow_oauth_cache=True)
		video = yt.streams.filter(only_audio=True).first()

		# download the file 
		out_file = video.download(output_path=directory) 
		base, ext = os.path.splitext(directory+"/"+out_file) 
	
		if sam_configuration:
			new_file = f"{artist} - {track}.m4a"
			new_file = new_file.replace("/","_")
		else:
			new_file = "" + track + "_" + artist + '.m4a'
			new_file = new_file.replace(" ","_")
			new_file = new_file.replace("/","_")
		
		os.rename(out_file, directory+"/"+new_file)  

		total_file = f"{directory}/{new_file}"	

		scrubber.m4a_to_mp3(total_file)

		total_file_mp3 = f"{total_file[:-4]}.mp3"		

		if total_data is None:
			scrubber.add_metadata(total_file_mp3, artist, track)
		else:
			scrubber.add_metadata(total_file_mp3, artist, track, total_data['album'], total_data['track_number'], total_data['release_date'])
			scrubber.add_cover_art(total_file_mp3, total_data['album_art'])


		scrubber.fix_file(total_file_mp3, directory)
				
		if self.logging:
                        print("...CONVERTED {}.mp3".format(new_file[:-4]))

		os.remove(total_file)
