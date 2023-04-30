import re
import urllib.request
import os
import re
from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
import logging


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
	'outtmpl': 'downloads/%(id)s.%(ext)s',
	'noplaylist': True,
    'logger': MyLogger()
}
watch_re = re.compile('watch\?v=')
playlist_re = re.compile('playlist\\?list=')
alt_yt_link_re = re.compile('youtu.be/')
yt_watch_string = "https://www.youtube.com/watch?v="
yt_querry_string = "https://www.youtube.com/results?search_query="




def search(keyword:str):
	def clean_keyword(keyword:str):
		return keyword.rstrip().replace(" ", "+")

	clean_keyword = clean_keyword(keyword)
	html = urllib.request.urlopen(yt_querry_string + clean_keyword)
	videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	return yt_watch_string + videoIds[0]


def download(url:str):
	with YoutubeDL(ydl_opts) as ydl:
		ydl.download(url)
		logging.debug(f"Sucessfully downloaded {url}")
		

def find_video(input:str):
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

	

	
# Not used
def download_from_keyword(keyword:str):
	link = search(keyword)
	download(link)


# Not used
def file_exists(link):
	return os.path.exists(f"downloads/{link[-8:]}.mp3")
	

# Not used
def convert_to_mp3(mp4_path, mp3_path):
	clip = VideoFileClip(mp4_path)
	clip.audio.write_audiofile(mp3_path)
	clip.close()



if __name__ == '__main__':
	#vid = yt.search('nightcore blackout')
	print(find_video('https://www.youtube.com/watch?v=X-1SbC14LZ4'))
	#info  = yt.ydl.extract_info('https://www.youtube.com/playlist?list=PLDCF162D5581F9725', download=False, process=False)
	#print(info.keys())
	#print(info)
	#for item in info['entries']:
	#	print(item)
	#yt.ydl.download(info['webpage_url'])
	

