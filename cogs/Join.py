from discord.ext import commands
from discord import Embed
import asyncio


async def setup(bot):
	await bot.add_cog(Join(bot))


class Join(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="adds bot to your current voice channel can also use =j", aliases=['j'])
	async def join(self, ctx):
		player = self.bot.players[ctx.guild.id]
		player.main_ctx = ctx
		channel = ctx.author.voice.channel
		if channel == None:
			await ctx.send(embed=Embed.from_dict({"title": "Join", "description": "You must be in a voice channel to use this command"}))
			return
		
		await player.connect(channel)
		await ctx.send(embed=Embed.from_dict({"title": "Join", "description": "Hello"}))
		self.bot.log("Join", ctx.guild.id, ctx.author.id, ctx.author.name)