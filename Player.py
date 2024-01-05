
from  MyAudioSource import MyAudioSource
import discord.voice_client
import discord.ext.commands
from Song import Song
from typing import Optional, List
import utils
import asyncio
from SpaceManagement import handle_downloads_space
import random
discord.voice_client.VoiceClient
class Player(object):
	def __init__(self):
		self.VC = None
		self.que : List[Song] = []
		self.now_playing : Optional[Song] = None
		self.looping = False
		self.main_ctx : Optional[discord.ext.commands.Context] = None
		self.playback_speed = 1
		self.nightcore = False
		self.bassboost = False
		self.waiting_for_download = False


	@property
	def length(self):
		return len(self.que)


	async def connect(self, channel):
		if self.VC == None or not self.VC.is_connected():
			self.VC = await channel.connect()
		else:
			await self.VC.move_to(channel)
		asyncio.create_task(self.start_bot_auto_leave())
		return 


	async def disconnect(self):
		if self.VC == None or not self.VC.is_connected():
			return
		await self.VC.disconnect()


	async def start_bot_auto_leave(self):
		while self.VC:
			if len(self.VC.channel.members) <= 1:
				await self.leave()
				break

			await asyncio.sleep(300)


	async def leave(self):
		self.stop()
		await self.disconnect()
		self.reset()
		handle_downloads_space()

	
	def stop(self):
		self.VC.stop()


	def reset(self):
		self.VC = None
		self.que.clear()
		self.now_playing = None
		self.playback_speed = 1
		self.nightcore = False
		self.bassboost = False
		self.looping = False


	def queue(self, song:Song):
		self.que.append(song)


	def queue_list(self, songs):
		for song in songs:
			self.queue(song)


	def dequeue(self):

		if not self.que:
			return None
		else:
			ret = self.que.pop(0)
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


	def seek(self, time):
		self.VC.pause()
		self.VC.source.seek(time)
		self.VC.resume()

	def remove(self, index):
		return self.que.pop(index)


	def shuffle(self):
		random.shuffle(self.que)


	def __str__(self):
		message = ''
		playback_string = ''
		total_durration = 0
		if self.playback_speed != 1:
			playback_string += f"Playback speed: {self.playback_speed * 100:.0f}%\n"
		if self.now_playing != None:
			message += f"Now Playing:\n{self.now_playing} {utils.seconds_to_time(int(self.now_playing.current_time))}/{utils.seconds_to_time(self.now_playing.length)}\n{playback_string}"

		if self.is_empty() and not self.looping:
			message += "Queue is empty"

		else:
			message += f"Up next{' in loop' if self.looping else ''}:"
			for i, song in enumerate(self.que):
				message += f"{i + 1}. {song} {utils.seconds_to_time(song.length / self.playback_speed)}\n"
				total_durration += song.length
				
			message += f"Durration: {utils.seconds_to_time(total_durration / self.playback_speed)}"
			
		return message


	def __repr__(self):
		ret = ""
		for item in self.que:
			ret += item.title
			ret += '\n'
		return ret

	# Play 
	def play_song(self):
		self.now_playing = self.dequeue()
		self.waiting_for_download = True
		self.now_playing.download()
		self.waiting_for_download = False
		if self.VC == None or not self.VC.is_connected():
			return
		self.VC.play(MyAudioSource(self.now_playing, self.playback_speed, self.nightcore, self.bassboost), after=self.play_next)
		

	def play_next(self, _):
		if self.looping and self.now_playing != None:
			self.queue(self.now_playing)
	
		if self.VC == None:
			return
		elif self.VC.is_playing():
			return
		elif self.is_empty():
			self.now_playing = None
			return
		elif self.waiting_for_download:
			return
		else:
			self.now_playing = None
			self.play_song()
