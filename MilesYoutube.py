import re
import urllib.request
import os
import re
from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import Song


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [
		{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    	},
		{'key': 'FFmpegMetadata'}
	],
	'outtmpl': 'downloads/%(id)s.%(ext)s',
	'noplaylist': True,
	'cookiefile': 'cookies.txt',
    'logger': MyLogger(),
	'quiet': True
}
soundcloud_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [
		{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    	},
		{'key': 'FFmpegMetadata'}
	],
	'outtmpl': 'downloads/%(id)s.%(ext)s',
	'noplaylist': True,
    'logger': MyLogger(),
	'quiet': True
}
watch_re = re.compile(r'(https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11})')
playlist_re = re.compile(r'(https?://(?:www\.)?youtube\.com/playlist\?list=[a-zA-Z0-9_-]+)')
alt_yt_link_re = re.compile(r'(https?://(?:www\.)?youtu\.be/[a-zA-Z0-9_-]{11})')
yt_watch_string = "https://www.youtube.com/watch?v="
yt_querry_string = "https://www.youtube.com/results?search_query="
soundcloud_regex = re.compile(r'^(?:https?://)?(?:www\.)?soundcloud\.com/[\w-]+/[\w-]+(?:\?.*)?$', re.IGNORECASE)




def search(keyword:str):
	def clean_keyword(keyword:str):
		return keyword.rstrip().replace(" ", "+")

	clean_keyword = clean_keyword(keyword)
	html = urllib.request.urlopen(yt_querry_string + clean_keyword)
	videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	return yt_watch_string + videoIds[1]


def download(url:str):
	opts = ydl_opts
	if soundcloud_regex.search(url):
		opts = soundcloud_opts
	with YoutubeDL(opts) as ydl:
		ydl.download(url)
		logging.debug(f"Sucessfully downloaded {url}")
		

def find_video(input:str):
	if soundcloud_regex.search(input):
		with YoutubeDL(soundcloud_opts) as ydl:
			return (ydl.extract_info(input, download=False, process=False),)
	with YoutubeDL(ydl_opts) as ydl:
		# for links of only one video
		alt_youtube_link = alt_yt_link_re.search(input)
		watch_link = watch_re.search(input)
		if alt_youtube_link or watch_link:
			video_id = ( input.partition('youtu.be/') if alt_youtube_link else input.partition('watch?v='))[2][:11]
			return (ydl.extract_info(yt_watch_string + video_id, download=False, process=False),)

		# for playlist links
		playlist_search = playlist_re.search(input)
		if playlist_search:
			info = ydl.extract_info(input, download=False, process=False)
			return list(info['entries'])
		

		return (ydl.extract_info(search(input), download=False, process=False),)


if __name__ == '__main__':
	song = Song.Song(find_video("https://soundcloud.com/yaaa03/dont_stop_the_music"))
	print(song.is_downloaded)
	print(song.length)
	song.download()
	

