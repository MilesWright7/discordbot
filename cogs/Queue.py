from discord.ext import commands
from discord import Embed
import utils


def setup(bot):
	bot.add_cog(Queue(bot))


class Queue(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="displayes queued songscan also use =q", aliases=["q"])
	async def queue(self, ctx):
		if not self.bot.VC:
			await ctx.send(embed=Embed.from_dict({"title": "Queue", "description": "Must connect bot to a voice channel first using '=join'"}))
			return

		message = ''
		playback_string = ''
		total_durration = 0
		if self.bot.playback_speed != 1:
			playback_string += f"Playback speed: {self.bot.playback_speed * 100:.0f}%"
		if self.bot.now_playing != None:
			message += f"Now Playing:\n[{self.bot.now_playing.title}]({self.bot.now_playing.url}) {utils.seconds_to_time(int(self.bot.now_playing.current_time))}/{utils.seconds_to_time(self.bot.now_playing.length / self.bot.VC.source.playback_speed)}\n{playback_string}\n"

		if self.bot.player.is_empty() and not self.bot.looping:
			message += "Queue is empty"
		elif self.bot.looping:
			message += "Up next in loop: \nuse '=sl' to stop looping\n"
			i = -1
			for i, song in enumerate(self.bot.player.que):
				message += f"{i + 1}. [{song.title}]({song.url}) {utils.seconds_to_time(song.length / self.bot.playback_speed)}\n"
				total_durration += song.length
				
			message += f"Durration of loop: {utils.seconds_to_time(total_durration / self.bot.playback_speed)}"

		else:
			message += f"Songs in queue:\n"
			total_durration = 0
			for i, song in enumerate(self.bot.player.que):
				message += f"{i + 1}. [{song.title}]({song.url}) {utils.seconds_to_time(self.bot.player.que[i].length / self.bot.playback_speed)}\n"
				total_durration += song.length
			message += f"Durration of queue: {utils.seconds_to_time(total_durration / self.bot.playback_speed)}"

		# discord throws error if embed message length > 6000
		if len(message) > 1500:
			message = message[: message.find("\n", 1500)]
			message += f"\nAnd more...\nDurration of queue: {utils.seconds_to_time(total_durration / self.bot.playback_speed)}"

		e=Embed.from_dict({
			"title":"Queue",
			"description":f"{message}",
			})
		await ctx.send(embed=e)