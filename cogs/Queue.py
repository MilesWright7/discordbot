from discord.ext import commands
from discord import Embed
import utils


async def setup(bot):
	await bot.add_cog(Queue(bot))


class Queue(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(help="displayes queued songscan also use =q", aliases=["q"])
	async def queue(self, ctx):

		player = self.bot.players[ctx.guild.id]

		if not player.VC:
			await ctx.send(embed=Embed.from_dict({"title": "Queue", "description": "Must connect bot to a voice channel first using '=join'"}))
			return

		message = str(player)
		# discord throws error if embed message length > 6000
		if len(message) > 1500:
			message = message[: message.find("\n", 1500)]
			message += f"\nAnd more..."

		e=Embed.from_dict({
			"title":"Queue",
			"description":f"{message}",
			})
		await ctx.send(embed=e)