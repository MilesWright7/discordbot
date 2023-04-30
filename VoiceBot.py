"""
A discord music bot with some other functionality. Poorly put together.
Mainly made using the depricated discord.py library.
Authored by Miles Wright
"""
import discord
import os
from dotenv import load_dotenv
import logging
from discord.ext import commands
from Player import Player
from Song import Song


class VoiceBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="=", case_insensitive=True, intents=discord.Intents().all())
		self.players = {}


	@staticmethod
	def log(command, guild_id, *kwargs):
		message = f"{command} {guild_id}"

		for arg in kwargs:
			message += f" {arg}"

		logging.info(message)


	async def on_ready(self):
		await self.init()
		await self.change_presence(status=discord.Status.online, activity=discord.Game("@Miles if I break"));
		logging.debug("Voice bot online!")


	async def on_guild_join(self, guild):
		self.players[guild.id] = Player()


	async def init(self):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, 'cogs/')
		extensions = os.listdir(filename)
		self.players = self.create_players()

		logging.debug('Started loading cogs ...')
		for file in extensions:
			if file.startswith('__'):
				pass
			else:
				cog = file.split('.')[0]
				await self.load_extension(f'cogs.{cog}')
		logging.debug('Successfully loaded all cogs!')


	@staticmethod
	def new_song(yt_obj):
		return Song(yt_obj)


	def create_players(self):
		players = {}
		for guild in self.guilds:
			players[guild.id] = Player()

		return players


def main():
	
	logging.basicConfig(filename="log.txt", level=logging.INFO,
					format="%(asctime)s %(message)s",
					datefmt='%Y-%m-%d %H:%M:%S')
	
	# turn off random logging from requests and such
	for value in logging.Logger.manager.loggerDict.values():
		if isinstance(value, logging.PlaceHolder):
			continue
		else:
			value.setLevel(logging.CRITICAL)
	logging.getLogger().addHandler(logging.StreamHandler())
	load_dotenv()
	token = os.getenv('DISCORD_TOKEN')

	bot = VoiceBot()
	bot.run(token)

if __name__ == "__main__":
	main()
