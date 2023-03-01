from discord.ext import commands
from discord import Embed
import subprocess

restart_script = "../start_bot.sh"
def setup(bot):
	bot.add_cog(Restart(bot))


class Restart(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="restarts the bot. Only use this if its dying and Miles isn't here to help you")
	async def restart(self, ctx):
		await ctx.send(embed=Embed.from_dict({"title": "Reset", "description": "Hard resetting the bot. Hopefully it will work soon."}))
		subprocess.Popen(restart_script)
