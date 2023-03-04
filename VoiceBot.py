"""
A discord music bot with some other functionality. Poorly put together.
Mainly made using the depricated discord.py library.
Authored by Miles Wright
"""
import discord
import os
from dotenv import load_dotenv
import pytube
import MilesYoutube
import logging
import random
from discord.ext import commands


class VoiceBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="=", case_insensitive=True)
		
		self.default_game = discord.Game("@Miles if I break")
		self.player = None
		self.VC = None
		self.yt = MilesYoutube.YT()
		self.now_playing = None
		self.looping = False
		self.main_ctx = None
		self.playback_speed = 1
		self.nightcore = False
		self.waiting_for_download = False


	@staticmethod
	def log(command, *kwargs):
		message = f"{command}"

		for arg in kwargs:
			message += f" {arg}"

		logging.info(message)


	async def on_ready(self):
		await self.init()
		await self.change_presence(status=discord.Status.online, activity=self.default_game);
		logging.info("Voice bot online!")


	async def init(self):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, 'cogs/')
		extensions = os.listdir(filename)

		logging.info('Started loading cogs ...')
		for file in extensions:
			if file.startswith('__'):
				pass
			else:
				cog = file.split('.')[0]
				self.load_extension(f'cogs.{cog}')
		logging.info('Successfully loaded all cogs!')

	def reset_defaults(self):
		
			self.player = None
			self.now_playing = None
			self.looping = False
			self.playback_speed = 1
			self.nightcore = False
			self.VC = None



	def ensure_player(self):
		if self.player == None:
			self.player = Player()


	@staticmethod
	def new_song(yt_obj):
		return Song(yt_obj)


	@staticmethod
	def new_playlist(yt_obj):
		return PlaylistObj(yt_obj)

	
class Song(object):
	folder = 'downloads/'

	def __init__(self, yt_obj : pytube.YouTube):
		self.title = yt_obj.title
		self.url = yt_obj.watch_url
		self.video_id = yt_obj.video_id
		self.yt_obj = yt_obj
		self.length = yt_obj.length
		self.current_time = 0
		self.age_restricted = yt_obj.age_restricted
		if self.age_restricted:
			self.yt_obj.use_oauth = True
			self.yt_obj.bypass_age_gate()


	def __repr__(self):
		return self.title


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
				print(f"Unable to download video {self.yt_obj.watch_url}\n {e}\n")
			VoiceBot.log("Download", self.title, self.length)


	def __eq__(self, other):
		if not other:
			return False
		return self.video_id == other.video_id

	
	def __ne__(self, other):
		return not self.__eq__(other)

class PlaylistObj(object):
	def __init__(self, yt_obj):
		self.song_list = [Song(x) for x in yt_obj.videos]


	def get_song_list(self):
		return self.song_list


class Player(object):
	def __init__(self):
		self.que = []
		self.isPlaying = False
		self.length = 0


	def queue(self, song:Song):
		self.que.append(song)
		self.length += 1


	def queue_list(self, songs):
		for song in songs:
			self.queue(song)


	def dequeue(self):

		if not self.que:
			return None
		else:
			ret = self.que.pop(0)
			self.length -= 1
			return ret


	def insert(self, song, index):
		self.que.insert(index, song)


	def clear(self):
		self.que.clear()
	

	def is_empty(self):
		if self.que:
			return False
		else:
			return True


	def remove(self, index):
		self.length -= 1
		return self.que.pop(index)


	def shuffle(self):
		random.shuffle(self.que)


	def __repr__(self):
		ret = ""
		for item in self.que:
			ret += item.title
			ret += '\n'
		return ret


def main():
	
	logging.basicConfig(filename="log.txt", level=logging.DEBUG,
					format="%(asctime)s %(message)s",
					datefmt='%Y-%m-%d %H:%M:%S')
	
	# turn off random logging from requests and such
	for value in logging.Logger.manager.loggerDict.values():
		if isinstance(value, logging.PlaceHolder):
			continue
		else:
			value.setLevel(logging.CRITICAL)
	logging.getLogger().addHandler(logging.StreamHandler())
	load_dotenv()
	token = os.getenv('DISCORD_TOKEN')

	bot = VoiceBot()
	bot.run(token)

if __name__ == "__main__":
	main()
