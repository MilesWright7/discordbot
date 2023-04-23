
import pytube	
import MilesYoutube
import os

class Song(object):
	folder = 'downloads/'

	def __init__(self, yt_obj : pytube.YouTube):
		self.yt_obj = yt_obj
		self.current_time = 0
		self.age_restricted = yt_obj.age_restricted
		if self.age_restricted:
			self.yt_obj.use_oauth = True
			self.yt_obj.bypass_age_gate()


	@property
	def title(self):
		try:
			return self.yt_obj.title
		except:
			stream = self.yt_obj.streams.first()
			return self.yt_obj.title


	@property
	def url(self):
		try:
			return self.yt_obj.watch_url
		except:
			stream = self.yt_obj.streams.first()
			return self.yt_obj.watch_url

	
	@property
	def length(self):
		try:
			return self.yt_obj.length
		except:
			stream = self.yt_obj.streams.first()
			return self.yt_obj.length

	
	@property
	def video_id(self):
		try:
			return self.yt_obj.video_id
		except:
			stream = self.yt_obj.streams.first()
			return self.yt_obj.video_id


	def location(self):
		string = self.folder
		string += self.video_id
		string += ".mp3"
		return string


	def is_downloaded(self):
		return os.path.exists(self.location())


	def download(self):
		if not self.is_downloaded():
			try:
				MilesYoutube.download_from_pytube(self.yt_obj)
			except BaseException as e:
				print(f"Unable to download video {self.url}\n {e}\n")
			#VoiceBot.log("Download", self.title, self.length)


	def __eq__(self, other):
		if not other:
			return False
		return self.video_id == other.video_id

	
	def __ne__(self, other):
		return not self.__eq__(other)


	def __str__(self):
		return f"[{self.title}]({self.url})"


	def __repr__(self):
		return self.title