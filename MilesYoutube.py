import re
import urllib.request
import os
import pytube
import re
from pytube.innertube import InnerTube
import pathlib

class YT:

	watch_re = re.compile('watch\\?v=')
	playlist_re = re.compile('list=')
	alt_yt_link_re = re.compile('youtu.be/')
	yt_watch_string = "https://www.youtube.com/watch?v="
	yt_querry_string = "https://www.youtube.com/results?search_query="

	def search(this, keyword:str):
		clean_keyword = this.clean_keyword(keyword)
		html = urllib.request.urlopen(this.yt_querry_string + clean_keyword)
		videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
		return this.yt_watch_string + videoIds[0]

	def download_from_url(this, url:str, ):
		yt = pytube.YouTube(url)
		out_file = None
		out_file = yt.streams.get_audio_only().download(output_path = 'downloads/')

		if out_file == None:
			out_file = yt.streams.get_lowest_resolution.download(filename = url[-8:], output_path = 'downloads/')
		new_file = f"downloads/{url[-8:]}.mp3"
		os.rename(out_file, new_file)
		print(f"Sucessfully downloaded {yt.title}")
		
	def clean_keyword(this, keyword:str):
		return keyword.rstrip().replace(" ", "+")

	def download_from_keyword(this, keyword:str):
		link = this.search(keyword)
		this.download_from_url(link)

	def file_exists(this, link):
		return os.path.exists(f"downloads/{link[-8:]}.mp3")
	
	def find_video(this, input:str):
		is_link = False
		is_playlist = False

		# for links of the form youtu.be/<video_id>
		alt_youtube_link = this.alt_yt_link_re.search(input)
		if alt_youtube_link:
			input = this.yt_watch_string + input[alt_youtube_link.span()[1]:]
			is_link = True

		# for playlist links
		playlist_search = this.playlist_re.search(input)
		if playlist_search:
			is_playlist = True

		# for standard youtube.com/watch... links
		watch_search = this.watch_re.search(input)
		if watch_search:
			is_link = True

		if is_playlist:
			try:
				pl = pytube.Playlist(input)
				if pl:
					return pl.videos

			except:
				pass
		if is_link:
			try:
				vid = pytube.YouTube(input)
				return [vid]
			except:
				pass

		return [pytube.YouTube(this.search(input))]

		
def download_from_pytube(yt_obj:pytube.YouTube):
	out_file = None
	out_file = yt_obj.streams.get_audio_only().download(output_path = 'downloads/')

	new_file = f"downloads/{yt_obj.video_id}.mp3"
	os.rename(out_file, new_file)

if __name__ == '__main__':
	yt = YT()
	#vid = pytube.YouTube("https://www.youtube.com/watch?v=N3zvFU49u08", use_oauth=True)
	pl = pytube.Playlist("https://youtube.com/playlist?list=PLTF9eI6zR7Tl3T_mGNNxX3VSP6sXaFlv_")

	print(pl.videos[:10])
	
	#download_from_pytube(vid)
	

