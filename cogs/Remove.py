from discord.ext import commands
from discord import Embed


async def setup(bot):
	await bot.add_cog(Remove(bot))


class Remove(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Removes songs at specified indexes in the queue")
	async def remove(self, ctx, index):
		
		player = self.bot.players[ctx.guild.id]
		try:
			idx = int(index)
		except ValueError:
			await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": "Numbers only!"}))
			return

		if (abs(idx) > player.length):
			await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": "Number larger than the queue"}))
			return

		if(idx >= 0):
			song = player.remove(idx - 1)
		else:
			song = player.remove(idx)

		message = f"Removed {idx}. {song})"
		
		await ctx.send(embed=Embed.from_dict({"title": "Remove", "description": message}))