from discord.ext import commands
from discord import Embed
import asyncio


def setup(bot):
	bot.add_cog(Join(bot))


class Join(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="adds bot to your current voice channel can also use =j", aliases=['j'])
	async def join(self, ctx):
		self.bot.main_ctx = ctx
		channel = ctx.author.voice.channel
		if channel == None:
			await ctx.send(embed=Embed.from_dict({"title": "Join", "description": "You must be in a voice channel to use this command"}))
			return
		self.bot.ensure_player()
		if self.bot.VC == None or not self.bot.VC.is_connected():
			self.bot.VC = await channel.connect()
		else:
			mama = self.bot.VC.voice_clients
			await self.bot.VC.move_to(channel)
		await ctx.send(embed=Embed.from_dict({"title": "Join", "description": "Hello"}))
		self.bot.log("Join", ctx.author.id, ctx.author.name)
		asyncio.create_task(self.start_bot_auto_leave())


	async def start_bot_auto_leave(self):
		# sometimes the VC.channel.members returns with only the bot inside when I am in the call. Unsure why that happens.
		while self.bot.VC:
			if len(self.bot.VC.channel.members) <= 1:
				leave = self.bot.get_cog("Leave")
				await leave.leave(self.bot.main_ctx)
				break

			await asyncio.sleep(300)