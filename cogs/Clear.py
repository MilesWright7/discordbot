from discord.ext import commands
from discord import Embed


async def setup(bot):
	await bot.add_cog(Clear(bot))


class Clear(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="Clear the queue can also use =c", aliases=["c"])
	async def clear(self, ctx):
		player = self.bot.players[ctx.guild.id]
		if player.looping:
			loop = self.bot.get_cog("Loop")
			await loop.stoploop(ctx)
		player.clear()
		await ctx.send(embed=Embed.from_dict({"title": "Clear", "description": "Queue cleared"}))