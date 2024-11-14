from discord.ext import commands
from discord import Embed


async def setup(bot):
	await bot.add_cog(Filters(bot))


class Filters(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="Sets playback speed to value given", aliases=["speed"] )
	async def playbackspeed(self, ctx, speed : float):
		try:
			as_float = float(speed)
		except:
			await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": "Invalid Input! Input must be a number between 0.5 and 2.0"}))
			return

		if as_float > 2.0 or as_float < 0.5:
			await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": "Invalid Input! Input must be a number between 0.5 and 2.0"}))
			return
		
		player = self.bot.players[ctx.guild.id]
		player.playback_speed = as_float
	
		await ctx.send(embed=Embed.from_dict({"title": "Playback Speed", "description": f"Set playback speed to {as_float * 100:.0f}%\nWill take effect next song that starts"}))


	@commands.hybrid_command(help="Toggle nightcore filter", aliases=["nc"])
	async def nightcore(self, ctx, on : bool | None):
		player = self.bot.players[ctx.guild.id]
		if on:
			player.nightcore = on
		else:
			player.nightcore = not player.nightcore
		
		player.playback_speed = 1.15 if player.nightcore else 1
		await ctx.send(embed=Embed.from_dict({"title": "Nightcore", "description": f"Toggled {'On' if player.nightcore else 'Off'}"}))

		
	@commands.hybrid_command(help="Toggle bassboost filter", aliases=["bb"])
	async def bassboost(self, ctx, on : bool | None):
		player = self.bot.players[ctx.guild.id]
		if on:
			player.bassboost = on
		else:
			player.bassboost = not player.bassboost
		
		await ctx.send(embed=Embed.from_dict({"title": "Bassboost", "description": f"Toggled {'On' if player.bassboost else 'Off'}"}))