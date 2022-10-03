from discord.ext import commands
from discord import Embed
from MyAudioSource import MyAudioSource
import utils


def setup(bot):
	bot.add_cog(Play(bot))


class Play(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="adds song to queue can also use =p", aliases=["p"])
	async def play(self, ctx, *, arg = None):
	
		if not self.bot.VC:
			join = self.bot.get_cog("Join")
			await join.join(ctx)

		elif not self.is_in_channel_with_bot(ctx):
			await ctx.send(embed=Embed.from_dict({"title": "Play", "description": "You are not in the same voice channel"}))
			return

		if arg == None:
			await ctx.send(content="Must supply a song name/url/search terms after the command\n", embed=Embed.from_dict({"title":"Example",
																																  "description": "=play low rider"}))
			return
		
		yt_obj, is_playlist = self.bot.yt.find_video(arg)
		if not is_playlist:
			song = self.bot.new_song(yt_obj)
			self.bot.player.queue(song)
			e = Embed.from_dict({"title": "Play",
					"description":f"Added [{song.title}]({song.url}) {utils.seconds_to_time(song.length)}"
					})
			self.bot.log("Play", ctx.author.id, ctx.author.name, song.title, song.length, song.is_downloaded())
		else:
			pl = self.bot.new_playlist(yt_obj)
			songs = pl.get_song_list()
			message = ""
			for song in songs:
				message += f"Added [{song.title}]({song.url}) {utils.seconds_to_time(song.length)}\n"
				self.bot.log("Play", ctx.author.id, ctx.author.name, song.title, song.length, song.is_downloaded())
			if message == "":
				message = "Doesn't work for auto generated playlists like My Mix or song radio. Sorry :("
			self.bot.player.queue_list(songs)
			if len(message) > 1500:
				message = message[: message.find("\n", 1500)]
				message += "\nAnd more..."
			e = Embed.from_dict({"title": "From Playlist", 
										 "description": message})
	
		await ctx.send(embed=e)
		if self.bot.VC.is_playing():
			pass
		else:
			self.play_next(None)

	
	def play_song(self):
		self.bot.now_playing = self.bot.player.dequeue()
		self.bot.now_playing.download()
		if self.bot.VC == None:
			return
		self.bot.VC.play(MyAudioSource(self.bot.now_playing, self.bot.playback_speed, self.bot.nightcore), after=self.play_next)
		

	def play_next(self, _):
		if self.bot.player == None:
			self.bot.now_playing = None
			return

		if self.bot.looping and self.bot.now_playing != None:
			self.bot.player.queue(self.bot.now_playing)
	
		if self.bot.VC == None:
			return
		elif self.bot.VC.is_playing():
			return
		elif self.bot.player.is_empty():
			self.bot.now_playing = None
			return
		else:
			self.bot.now_playing = None
			self.play_song()

			
	def is_in_channel_with_bot(self, ctx):
		channel = ctx.author.voice.channel
		return channel == self.bot.VC.channel