import discord
import os
import youtube_dl
from dotenv import load_dotenv
import youtube
import asyncio
import random

from discord.ext import commands

class Song(object):
    folder = 'downloads/'
    downloaded = False
    
    def __init__(self, meta):
        self.title = meta['title']
        self.duratoin = meta['duration']
        self.url = meta['webpage_url']

    def __repr__(self):
        return self.title

    def location(self):
        string = self.folder
        string += self.title.replace(' ', '_')
        string = string.replace('\'s', '_s')
        for ch in ['\\', ']', '[', '(', ')', '}', '{', '\'', '\"']:
            if ch in string:
                string = string.replace(ch, '')
        string += ".mp3"
        return string


class Player(object):

    def __init__(self, channel):
        self.que = []
        self.isPlaying = False
        self.channel = channel
        self.length = 0

    def queue(self, song):
        self.que.append(song)
        self.length += 1

    def dequeue(self):
        if not self.que:
            return None
        else:
            ret = self.que.pop(0)
            self.length -= 1
            return ret

    def clear(self):
        self.que.clear()
    
    def isempty(self):
        if self.que:
            return False
        else:
            return True


    def __repr__(self):
        ret = ""
        for item in self.que:
            ret += item.title
            ret += '\n'
        return ret

print('dab')
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')

print('dab')
client = commands.Bot(command_prefix = '=')

game = discord.Game("pizza time")


player = None
yt = youtube.Youtube()

@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=guild)
    print(f'{client.user} has connected to Discord!\n'
            f'{server.name}(id: {server.id})')
    await client.change_presence(status=discord.Status.online, activity=game);
    """
    while(1):
        if player:
            while not player.isempty():
                if not player.isPlaying:
                    for VC in client.voice_clients:
                        if player.channel == VC.channel:
                            song = player.dequeue
                            if song:
                                player.isPlaying = True
                                VC.play(discord.FFmpegPCMAudio(song.location()), after=lambda: print('done'))
                                player.isPlaying = False
                            else:
                                print("tried to play song but player was empty")

    """


@client.command(help="you say bruh i say <:FazeUp:555302712007196672>" )
async def bruh(ctx):
    await ctx.send("<:FazeUp:555302712007196672>")

@client.command(help="roll <low> <high>")
async def roll(ctx, arg1, arg2):
    ctx.send('{} rolled a  {}'.format(ctx.author.mention, random.randint(arg1, arg2))) 

@client.command(help="adds bot to your current voice channel")
async def join(ctx):
    channel = ctx.author.voice.channel
    VC = await channel.connect()

@client.command(help="bot leaves")
async def leave(ctx):
    channel = ctx.author.voice.channel
    for VC in client.voice_clients:
        if channel == VC.channel:
            await VC.disconnect()
            return
    else:
        await ctx.send("Not in voice channel")

@client.command(help="displayes queued songs")
async def queue(ctx):
    global player
    que = ''
    if not player:
        player = Player(ctx.author.voice.channel)
    if player.isempty():
        message = "Queue is empty"
    else:
        message = 'Songs in queue:'
        for item in player.que:
            que += item.title
            que += '\n'
    e=discord.Embed.from_dict({
        "title":f"{message}",
        "description":f"{que}",
        })
    await ctx.send(embed=e)
    

@client.command(help="adds song to queue")
async def play(ctx, *, arg):
    channel = ctx.author.voice.channel
    global player
    if not player:
        player = Player(channel)
    for VC in client.voice_clients:
        if channel == VC.channel:
            meta = yt.search(arg)
            song = Song(meta)
            yt.download(song.url)
            e=discord.Embed.from_dict({
                "description":f"Added {song.title} to queue",
                })
            player.queue(song)
            await ctx.send(embed=e)
            if VC.is_playing():
                pass

            else:
                play_next(VC)

        else:
            await ctx.send("You are not in a voice channel")


def play_next(VC):
    if VC.is_playing():
        pass
    else:
    
        VC.play(discord.FFmpegPCMAudio(player.dequeue().location()), after=lambda VC: play_next(VC))


print('dab')
client.run(token)


