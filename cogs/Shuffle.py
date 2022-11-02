from discord.ext import commands
from discord import Embed


def setup(bot):
	bot.add_cog(Shuffle(bot))


class Shuffle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Mixes up upcomming songs")
	async def shuffle(self, ctx):
		self.bot.player.shuffle()
		await ctx.send(embed=Embed.from_dict({"title":"Shuffle", "description": "Queue shuffled"}))
	