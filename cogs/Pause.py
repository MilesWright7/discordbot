from discord.ext import commands
from discord import Embed
import discord


async def setup(bot):
	await bot.add_cog(Pause(bot))


class Pause(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="Pause current song", aliases=["stop"])
	async def pause(self, ctx : commands.Context):

		player = self.bot.players[ctx.guild.id]
		player.pause()
		await ctx.send(embed=Embed.from_dict({"title": "Pause", "description": "Audio paused"}))


	@commands.hybrid_command(help="Resumes song")
	async def resume(self, ctx : commands.Context):

		player = self.bot.players[ctx.guild.id]
		player.resume()
		await ctx.send(embed=Embed.from_dict({"title": "Resume", "description": "Audio resumed"}))


	@commands.hybrid_command(help="Skip current song", aliases=["s", "next", "n"])
	async def skip(self, ctx : commands.Context):

		player = self.bot.players[ctx.guild.id]
		if player.now_playing == None:
			await ctx.send(embed=Embed.from_dict({"title": "Skip", "description": "Nothing to skip"}))
			return
		await ctx.send(embed=Embed.from_dict({"title": "Skip", "description": f"Skipping {player.now_playing}"}))
		player.stop()