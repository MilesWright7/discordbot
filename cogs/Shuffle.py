from discord.ext import commands
from discord import Embed


async def setup(bot):
	await bot.add_cog(Shuffle(bot))


class Shuffle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Mixes up upcomming songs")
	async def shuffle(self, ctx):

		player = self.bot.players[ctx.guild.id]
		player.shuffle()
		await ctx.send(embed=Embed.from_dict({"title":"Shuffle", "description": "Queue shuffled"}))
	