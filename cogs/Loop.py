from discord.ext import commands
from discord import Embed


def setup(bot):
	bot.add_cog(Loop(bot))


class Loop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Loops queue, finished songs are added to the end. can also use =l", aliases=["l"])
	async def loop(self, ctx):
		self.bot.looping = True
		await ctx.send(embed=Embed.from_dict({"title": "Loop", "description": "Now looping"}))
		

	@commands.command(help="Turns off looping can also use =sl", aliases=["sl"])
	async def stoploop(self, ctx):
		self.bot.looping = False
		await ctx.send(embed=Embed.from_dict({"title": "Stop Loop", "description": "Looping stopped"}))