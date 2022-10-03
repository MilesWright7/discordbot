from discord.ext import commands
from discord import Embed
from SpaceManagement import handle_downloads_space


def setup(bot):
	bot.add_cog(Leave(bot))


class Leave(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="bot leaves")
	async def leave(self, ctx):
		try:
			await self.bot.VC.disconnect()
			self.bot.reset_defaults()
			handle_downloads_space()
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "Goodbye"}))
			self.bot.log("Leave", ctx.author.id, ctx.author.name)
		
		except:
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "I'm already gone"}))