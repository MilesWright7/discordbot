from ast import Dict, List
import os
from discord.ext import commands
from discord import Embed
import MilesYoutube
from VoiceBot import VoiceBot
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging


SAVE_PLAYLIST_PATH = "playlists.csv"

COMMANDS = {"play", "show", "remove", "add"}

async def setup(bot):
	await bot.add_cog(Playlist(bot))


class Playlist(commands.Cog):
	def __init__(self, bot: VoiceBot):
		self.bot = bot
		self.playlists = {}
		self.loaded = False
		asyncio.create_task(self.load_playlists())

	def get_info(self, id):
		yt_obj = []
		try:
			if(os.path.exists("downloads/" + id + ".mp3")):
				audio = EasyID3("downloads/" + id + ".mp3")
				mp3 = MP3("downloads/" + id + ".mp3")
				title = audio['title']
				length = mp3.info.length
				return {"id": id, "duration": length, "url": self.create_youtube_link(id), "title": title}
		
			else:
				try:
					yt_obj = MilesYoutube.find_video(self.create_youtube_link(id))[0]
				except Exception as e:
					logging.warning(e)
					if(os.path.exists("downloads/" + id + ".mp3")):
						return {"id": id, "duration": 200, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "Bofa Deez - Candice"}
					else:
						return None
				return yt_obj
		except Exception as e:
			logging.warning(e)
			return None
				
	
	async def load_playlists(self):
		with open(SAVE_PLAYLIST_PATH, 'r') as f:
			for entry in f:
				playlist = entry.strip().split(",")
				title = playlist.pop(0)
				self.playlists[title] = []

				loop = asyncio.get_running_loop()
				with ThreadPoolExecutor() as executor:
					tasks = [loop.run_in_executor(executor, self.get_info, id) for id in playlist]

					results = await asyncio.gather(*tasks)
				
				for item in results:
					if item:
						song = self.bot.new_song(item)
						self.playlists[title].append(song)	

				logging.info(f"Playlist {title} finished loading")

		logging.info("All playlists finished loading")
		self.loaded = True
		return


	def save_playlists(self):
		with open(SAVE_PLAYLIST_PATH, 'w') as f:
			f.writelines(self.generate_playlist_file_string())


	def generate_playlist_file_string(self):
		for key in self.playlists:
			string = key + ","+ ",".join(x.video_id for x in self.playlists[key])
			yield string
			yield "\n"


	def create_youtube_link(self, video_id):
		return f"https://www.youtube.com/watch?v={video_id}"


	def split_arg(self, arg:str):
		length = len(arg.split())

		if length > 2:
			return arg.split(" ", 2)

		if length == 2: 
			l = arg.split(" ", 1)
			l.append("")
			return l

		else:
			return [arg, "", ""]


	@commands.hybrid_command(help="Interact with the playlist feature", aliases=["pl"])
	async def playlist(self, ctx, *, arg=""):

		command, playlist_name, song = self.split_arg(arg)
		command = command.lower()
		playlist_name = playlist_name.lower()

		if not self.loaded:
			e=Embed.from_dict({"title":"Playlist","description":f"Playlists not loaded yet. Wait a bit before trying again.",}) 
			await ctx.send(embed=e)
			return
		
		# common user error. allow for swapped paramaterssa
		if not command in COMMANDS:
			if not playlist_name in COMMANDS:
				e=Embed.from_dict({"title":"Playlist","description":f"Usage: commands (add, remove, show, play), playlist name, song name\nFor example\n=playlist add dota2 low rider",}) 
				await ctx.send(embed=e)
				return

			tmp = command
			command = playlist_name
			playlist_name = tmp

		# ADD
		if command == "add":

			if not playlist_name:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Please provide a playlist name. For example...\n=playlist add dota2 low rider",
					})
				await ctx.send(embed=e)
				return
			

			if not song:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Please provide a song to add. For example...\n=playlist add **{playlist_name}** low rider",
					})
				await ctx.send(embed=e)
				return


			if not playlist_name in self.playlists:
				self.playlists[playlist_name] = []
				
			yt_list = MilesYoutube.find_video(song)
			message = ""
			for yt in yt_list:
				song = self.bot.new_song(yt)
				if not song in self.playlists[playlist_name]:
					self.playlists[playlist_name].append(song)
					message += f"{song}\n"

			if not message:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Did not add anything to playlist. Song could already be in playlist or possibly failed for some other reason",
					})
				await ctx.send(embed=e)
				return
			
			e=Embed.from_dict({
				"title":"Playlist",
				"description":f"Added the following songs to playlsit **{playlist_name}**\n{message}",
				})
			await ctx.send(embed=e)
			self.save_playlists()
			return
			
		
		# REMOVE
		elif command == "remove" or command == "delete" or command == "del" or command == "rm":
			if not playlist_name:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Please provide a playlist name. For example...\n=playlist remove dota2 low rider",
					})
				await ctx.send(embed=e)
				return
			
			if not playlist_name in self.playlists:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"That playlist does not exist. Show all playlists by using =playlist show",
					})
				await ctx.send(embed=e)
				return

			if not song:
				del self.playlists[playlist_name]
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Removed playlist **{playlist_name}**",
					})
				await ctx.send(embed=e)
				self.save_playlists()
				return

			
			yt_list = MilesYoutube.find_video(song)
			if len(yt_list) > 1:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Please only remove one song at a time because I'm stupid and lazy",
					})
				await ctx.send(embed=e)
				return

			for yt in yt_list:
				song = self.bot.new_song(yt)
				if not song in self.playlists[playlist_name]:
					e=Embed.from_dict({
						"title":"Playlist",
						"description":f"Song not in playlist, but thats good right?",
					})
					await ctx.send(embed=e)
					return
				else:
					self.playlists[playlist_name].remove(song)
					e=Embed.from_dict({
						"title":"Playlist",
						"description":f"Removed {song} from **{playlist_name}**",
					})
					await ctx.send(embed=e)
					self.save_playlists()
					return
		

		# SHOW
		elif command == "show" or command == "display":
			if playlist_name == "":
				names = "\n".join([x for x in self.playlists])
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"All playlists:\n{names}",
					})
				await ctx.send(embed=e)
				return

			if playlist_name not in self.playlists:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Cannot find playlist **{playlist_name}**",
					})
				await ctx.send(embed=e)
				return

			songs = self.playlists[playlist_name]
			message = "\n".join([f"{idx}. {song}" for idx, song in enumerate(songs, 1)])
			e=Embed.from_dict({
				"title":"Playlist",
				"description":f"Songs for playlist **{playlist_name}**\n{message}",
				})
			await ctx.send(embed=e)
			return


		# PLAY
		elif command == "play":
			if playlist_name == "":
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Please specify playlist to play from",
					})
				await ctx.send(embed=e)
				return

			
			if playlist_name not in self.playlists:
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Cannot find playlist **{playlist_name}**",
					})
				await ctx.send(embed=e)
				return

			else:
				player = self.bot.players[ctx.guild.id]
				if not player.VC or not player.VC.is_connected():
					join = self.bot.get_cog("Join")
					await join.join(ctx)

				songs = self.playlists[playlist_name]
				player.queue_list(songs)
				e=Embed.from_dict({
					"title":"Playlist",
					"description":f"Added songs from **{playlist_name}** to queue",
					})
				await ctx.send(embed=e)

				player.play_next(None)