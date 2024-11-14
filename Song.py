
import MilesYoutube
import os

class Song(object):
	folder = 'downloads/'

	def __init__(self, info):
		self.info = info
		self.current_time = 0


	@property
	def title(self):
		return self.info['title']


	@property
	def url(self):
		try:
			return self.info['url']
		except:
			return self.info['webpage_url']
	

	@property
	def length(self):
		return int(self.info['duration'])

	
	@property
	def video_id(self):
		return self.info['id']


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
				MilesYoutube.download(self.url)
			except BaseException as e:
				print(f"Unable to download video {self.url}\n {e}\n")


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