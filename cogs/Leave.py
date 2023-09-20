from discord.ext import commands
from discord import Embed
from SpaceManagement import handle_downloads_space


async def setup(bot):
	await bot.add_cog(Leave(bot))


class Leave(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="bot leaves")
	async def leave(self, ctx):
		player = self.bot.players[ctx.guild.id]
		try:
			await player.leave()
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "Goodbye"}))
			self.bot.log("Leave", ctx.guild.id, ctx.author.id, ctx.author.name)
		
		except:
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "I'm already gone"}))