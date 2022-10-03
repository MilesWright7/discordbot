from discord.ext import commands
from discord import Embed


def setup(bot):
	bot.add_cog(Remove(bot))


class Remove(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Removes songs at specified indexes in the queue")
	async def remove(self, ctx, index):
		try:
			idx = int(index)
		except ValueError:
			await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": "Numbers only!"}))
			return

		if (abs(idx) > self.bot.player.length):
			await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": "Number larger than the queue"}))
			return

		if(idx >= 0):
			song = self.bot.player.remove(idx - 1)
		else:
			song = self.bot.player.remove(idx)

		message = f"Removed {idx}. [{song.title}]({song.url})"
		
		await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": message}))