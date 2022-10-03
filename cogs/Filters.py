from discord.ext import commands
from discord import Embed


def setup(bot):
	bot.add_cog(Seek(bot))


class Seek(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Sets playback speed to value given", aliases=["speed"] )
	async def playbackspeed(self, ctx, speed):
		try:
			as_float = float(speed)
		except:
			await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": "Invalid Input! Input must be a number between 0.5 and 2.0"}))
			return

		if as_float > 2.0 or as_float < 0.5:
			await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": "Invalid Input! Input must be a number between 0.5 and 2.0"}))
			return
		
		self.bot.playback_speed = as_float
	
		await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": f"Set playback speed to {as_float * 100:.0f}%\nWill take effect next song that starts"}))


	@commands.command(help="Toggle nightcore filter")
	async def nightcore(self, ctx):
		self.bot.nightcore = not self.bot.nightcore
		
		self.bot.playback_speed = 1.15 if self.bot.nightcore else 1
		await ctx.send(embed=Embed.from_dict({"title": "Nightcore", "description": f"Toggled {'On' if self.bot.nightcore else 'Off'}"}))