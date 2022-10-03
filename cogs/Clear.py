from discord.ext import commands
from discord import Embed


def setup(bot):
	bot.add_cog(Clear(bot))


class Clear(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Clear the queue can also use =c", aliases=["c"])
	async def clear(self, ctx):
		if self.bot.looping:
			loop = self.bot.get_cog("Loop")
			await loop.stoploop(ctx)
		self.bot.player.clear()
		await ctx.send(embed=Embed.from_dict({"title": "Clear", "description": "Queue cleared"}))