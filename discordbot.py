import discord
import os
from dotenv import load_dotenv
import MilesYoutube
import asyncio
import random

from discord.ext import commands

class Song(object):
    folder = 'downloads/'
    downloaded = False
    
    def __init__(self, title, url, video_id):
        self.title = title
        self.duration = 0
        self.url = url
        self.video_id = video_id

    def __repr__(self):
        return self.title

    def location(self):
        string = self.folder
        string += self.video_id
        # string += self.title.replace(' ', '_')
        # string = string.replace('\'s', '_s')
        # for ch in ['\\', ']', '[', '(', ')', '}', '{', '\'', '\"']:
        #     if ch in string:
        #         string = string.replace(ch, '')
        string += ".mp3"
        return string

    def is_downloaded(self):
        os.path.exists(self.location)


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
    
    def is_empty(self):
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

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '=')
game = discord.Game("@Miles if I break")

empty_song = Song("", "", "")
player = None
VC = None
yt = MilesYoutube.YT()
now_playing = empty_song

@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=guild)
    print(f'{client.user} has connected to Discord!\n'
            f'{server.name}(id: {server.id})')
    await client.change_presence(status=discord.Status.online, activity=game);
    # while(1):
    #     if player:
    #         while not player.isempty():
    #             if not player.isPlaying:
    #                 for VC in client.voice_clients:
    #                     if player.channel == VC.channel:
    #                         song = player.dequeue
    #                         if song:
    #                             player.isPlaying = True
    #                             VC.play(discord.FFmpegPCMAudio(song.location()), after=lambda: print('done'))
    #                             player.isPlaying = False
    #                         else:
    #                             print("tried to play song but player was empty")

    


@client.command(help="you say bruh i say <:FazeUp:555302712007196672>" )
async def bruh(ctx):
    await ctx.send("<:FazeUp:555302712007196672>")

@client.command(help="roll <low> <high>")
async def roll(ctx, arg1 = 0, arg2 = 100):
    await ctx.send('{} rolled a  {}'.format(ctx.author.mention, random.randint(arg1, arg2))) 

@client.command(help="adds bot to your current voice channel")
async def join(ctx):
    channel = ctx.author.voice.channel
    global player
    player = Player(channel)
    global VC
    VC = await channel.connect()

@client.command(help="bot leaves")
async def leave(ctx):
    try:
        global VC
        await VC.disconnect()
        VC = None
        global player
        player = None
        
    except:
        await ctx.send("Not in voice channel")

@client.command(help="displayes queued songs")
async def queue(ctx):
    if not VC:
        ctx.send("Must connect bot to a voice channel first using \"join\"")
    que = ''
    if player.is_empty():
        message = "Queue is empty"
    else:
        message = f"Now Playing:\n[{now_playing.title}]({now_playing.url})\nSongs in queue:\n\n"
        for i, song in enumerate(player.que):
            message += f"{i + 1}. [{song.title}]({song.url})\n"
    e=discord.Embed.from_dict({
        "title":f"Queue",
        "description":f"{message}",
        })
    await ctx.send(embed=e)
    

@client.command(help="adds song to queue")
async def play(ctx, *, arg):
    channel = ctx.author.voice.channel
    
    if not is_in_channel_with_bot(ctx):
        await ctx.send("You are not in the same voice channel")
        return

    if not VC:
        ctx.send("Must connect bot to a voice channel first using \"join\"")
        return

    global player
    title, url, video_id = yt.download_from_keyword(arg)
    song = Song(title, url, video_id)
    e = discord.Embed.from_dict({
                "description":f"Added [{song.title}]({song.url}) to queue",
                })
    player.queue(song)
    await ctx.send(embed=e)
    if VC.is_playing():
        pass
    else:
        play_next(None)


def play_song():
    global now_playing
    now_playing = player.dequeue()
    VC.play(discord.FFmpegPCMAudio(now_playing.location()), after = play_next)

def play_next(e):
    global now_playing
    now_playing = empty_song
    if VC == None:
        return
    elif VC.is_playing():
        return
    elif player.is_empty():
        return
    else:
        play_song()


@client.command(help="Pause current song")
async def pause(ctx):
    VC.pause()

@client.command(help="Stop playing")
async def stop(ctx):
    VC.stop()

@client.command(help="Skip song")
async def skip(ctx):
    VC.stop()
    play_next(None)

@client.command(help="Resumes song")
async def resume(ctx):
    VC.resume()

@client.command(help="Clear the queue")
async def clear(ctx):
    global player
    player.clear()
    

def is_in_channel_with_bot(ctx):
    channel = ctx.author.voice.channel
    return channel == VC.channel

client.run(token)


