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
			self.bot.player = None
			self.bot.now_playing = None
			self.bot.looping = False
			self.bot.playback_speed = 1
			handle_downloads_space()
			await self.bot.VC.disconnect()
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "Goodbye"}))
			self.bot.log("Leave", ctx.author.id, ctx.author.name)
			self.bot.VC = None
		
		except:
			await ctx.send(embed=Embed.from_dict({"title": "Leave", "description": "I'm already gone"}))