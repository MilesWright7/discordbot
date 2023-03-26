from discord.ext import commands
from discord import Embed
import utils


async def setup(bot):
	await bot.add_cog(Seek(bot))


class Seek(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	@commands.command(help="seeks to time in current track", aliases=["jump"])
	async def seek(self, ctx, time):

		player = self.bot.players[ctx.guild.id]
		converted_time = utils.time_to_seconds(time)
		if converted_time < 0:
			await ctx.send(embed=Embed.from_dict({"title": "Seek", "description": "Provide a valid time format, format of minutes:seconds or only seconds\nFor example: =seek 150 or =seek 2:30"}))
			return

		if converted_time > player.now_playing.length:
			await ctx.send(embed=Embed.from_dict({"title": "Seek", "description": "Time specified is longer than current song's durration"}))
			return

		player.seek(converted_time)
		await ctx.send(embed=Embed.from_dict({"title": "Seek", "description": f"Playing {player.now_playing} {utils.seconds_to_time(int(player.now_playing.current_time))}/{utils.seconds_to_time(player.now_playing.length)}"}))


	@commands.command(help="skips the given amount of time in current track", aliases=["ff"])
	async def fastforward(self, ctx, time):

		player = self.bot.players[ctx.guild.id]
		converted_time = utils.time_to_seconds(time)
		if converted_time < 0:
			await ctx.send(embed=Embed.from_dict({"title": "Fast Forward", "description": "Provide a valid time format, format of minutes:seconds or only seconds\nFor example: =seek 150 or =seek 2:30"}))
			return
	
		seek_time = int(converted_time + player.now_playing.current_time)
		if seek_time > self.bot.now_playing.length:
			await ctx.send(embed=Embed.from_dict({"title": "Seek", "description": "Time specified is longer than current song's durration"}))
			return
	
		player.seek(seek_time)
		await ctx.send(embed=Embed.from_dict({"title": "Fast Forward", "description": f"Playing {player.now_playing} {utils.seconds_to_time(int(player.now_playing.current_time))}/{utils.seconds_to_time(player.now_playing.length)}"}))