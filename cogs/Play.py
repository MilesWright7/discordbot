from discord.ext import commands
from discord import Embed
import utils
import MilesYoutube

MAX_SONG_DURATION = 1200 #twenty minutes

async def setup(bot):
	await bot.add_cog(Play(bot))


class Play(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="adds song to queue can also use =p", aliases=["p"])
	async def play(self, ctx, *, arg : str | None = None):

		player = self.bot.players[ctx.guild.id]
	
		if not player.VC or not player.VC.is_connected():
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
		
		yt_list = MilesYoutube.find_video(arg)
		message = ""
		to_long_message_sent = False
		if len(yt_list) == 0:
			await ctx.send(embed=Embed.from_dict({"title": "Play", 
										 "description": "Some error happened. Couldn't find the playlist/song. Sorry"}))
			return
		
		for yt in yt_list:
			if yt['duration'] == None:
				await ctx.send(embed=Embed.from_dict({"title": "Play", 
										 "description": f"issue with {yt["url"]}. Could be private video or deleted video. Regardless it isn't working."}))
				continue
			song = self.bot.new_song(yt)
			if song.length > MAX_SONG_DURATION:
				if not to_long_message_sent:
					await ctx.send(embed=Embed.from_dict({"title": "Play", 
										 "description": f"{song} over 20 minutes. To queue longer songs become a supporter by sending Miles-Wright-6 a minimum of $20 on venmo :D"}))
					to_long_message_sent = True
				continue

			message += f"Added {song} {utils.seconds_to_time(song.length)}\n"
			self.bot.log("Play", ctx.guild.id, ctx.author.id, ctx.author.name, song.title, song.length, song.is_downloaded())
	
			player.queue(song)
			
		if len(message) > 1500:
			message = message[: message.find("\n", 1500)]
			message += "\nAnd more..."

		e = Embed.from_dict({"title": "Play", 
										 "description": message})
	
		if len(message) > 0:
			await ctx.send(embed=e)
			
		player.play_next(None)
			

	def is_in_channel_with_bot(self, ctx):
		channel = ctx.author.voice.channel
		return channel == self.bot.VC.channel
