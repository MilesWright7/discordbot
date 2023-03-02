from discord.ext import commands
from discord import Embed
from MyAudioSource import MyAudioSource
import utils
import os


class Sound(object):
	folder = 'downloads/sounds/'
	def __init__(self, name:str):
		self.name = name


	def location(self):
		string = self.folder + self.name + '.mp3'
		return string


	def exists(self):
		return os.path.exists(self.location())

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		return self.name == other.name


def setup(bot):
	sb = Soundboard(bot)
	sb.InitSounds()
	bot.add_cog(sb)


class Soundboard(commands.Cog):
	sounds_file = 'sounds.txt'
	def __init__(self, bot):
		self.bot = bot
		self.sounds = set()


	def InitSounds(self):
		with open(self.sounds_file, 'r') as f:
			for line in f:
				self.sounds.append(Sound(line.strip()))


	@commands.command(help="Add sound to soundboard", aliases=["as"])
	async def addsound(self, ctx, *, arg = None):
		if arg == None:
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Must supply name and sound file to play"}))
			return

		arg = arg.strip()
		if not ctx.message.attachments:
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Must supply name and sound file to play"}))
			return

		if len(ctx.message.attachments) != 1:
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Must supply only one sound file"}))
			return

		if not ctx.message.attachments[0].content_type is 'audio/mpeg':
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Must supply sound file only\nOnly supports .mp3 files"}))
			return


		sound = Sound(arg)
		filename:str = ctx.message.attachments[0].filename
		filename = arg + filename[filename.rindex("."):]
		await ctx.message.attachments[0].save(sound.location())





			
	@commands.command(help="Lists sounds added to soundboard", aliases=["ls"])
	async def listsounds(self, ctx):
		message = ", ".join([x.name for x in self.sounds])
		await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Sounds I know\n" + message}))

			
	@commands.command(help="Plays sound on soundboard", aliases=["ps"])
	async def playsound(self, ctx, *, arg = None):
		if arg == None:
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "Must supply sound to play"}))
			return
		
		arg = arg.strip()
		if not arg in self.sounds:
			await ctx.send(embed=Embed.from_dict({"title":"Soundboard", "description": "I don't have that sound"}))
			return

