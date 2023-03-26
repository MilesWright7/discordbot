from discord.ext import commands
import random


async def setup(bot):
	await bot.add_cog(Random(bot))


class Random(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		
	@commands.command(help="you say bruh i say <:FazeUp:555302712007196672>" )
	async def bruh(self, ctx):
		await ctx.send("<:FazeUp:555302712007196672>")


	@commands.command(help="roll <low> <high>")
	async def roll(self, ctx, arg1 = 0, arg2 = 100):
		await ctx.send('{} rolled a  {}'.format(ctx.author.mention, random.randint(arg1, arg2))) 