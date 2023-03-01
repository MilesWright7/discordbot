from discord.ext import commands
from discord import Embed
from MyAudioSource import MyAudioSource
import utils

MAX_SONG_DURATION = 1200 #twenty minutes

def setup(bot):
	bot.add_cog(Play(bot))


class Play(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="adds song to queue can also use =p", aliases=["p"])
	async def play(self, ctx, *, arg = None):
	
		if not self.bot.VC or not self.bot.VC.is_connected():
			join = self.bot.get_cog("Join")
			await join.join(ctx)

		## add back if abused
		#elif not self.is_in_channel_with_bot(ctx):
		#	await ctx.send(embed=Embed.from_dict({"title": "Play", "description": "You are not in the same voice channel"}))
		#	return

		if arg == None:
			await ctx.send(content="Must supply a song name/url/search terms after the command\n", embed=Embed.from_dict({"title":"Example",
																																  "description": "=play low rider"}))
			return
		
		yt_list = self.bot.yt.find_video(arg)
		message = ""
		to_long_message_sent = False
		if len(yt_list) == 0:
			await ctx.send(embed=Embed.from_dict({"title": "Play", 
										 "description": "Some error happened. Couldn't find the playlist/song. Sorry"}))
			return
		
		for yt in yt_list:
			song = self.bot.new_song(yt)
			if song.length > MAX_SONG_DURATION:
				if not to_long_message_sent:
					await ctx.send(embed=Embed.from_dict({"title": "Play", 
										 "description": "[{song.title}]({song.url}) over 20 minutes. To queue longer songs become a supporter by sending Miles-Wright-6 a minimum of $20 on venmo :D"}))
					to_long_message_sent = True
				continue

			message += f"Added [{song.title}]({song.url}) {utils.seconds_to_time(song.length)}\n"
			self.bot.log("Play", ctx.author.id, ctx.author.name, song.title, song.length, song.is_downloaded())
	
			self.bot.player.queue(song)
			
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
		if self.bot.VC == None or not self.bot.VC.is_connected():
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
