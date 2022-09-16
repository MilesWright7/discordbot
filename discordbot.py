"""
A discord music bot with some other functionality. Poorly put together.
Mainly made using the depricated discord.py library.
Authored by Miles Wright
"""
from functools import total_ordering
from sqlite3 import converters
import discord
import os
from dotenv import load_dotenv
import pytube
from pytube.contrib.playlist import Playlist
import MilesYoutube
import asyncio
import random
from time import sleep
from SpaceManagement import handle_downloads_space
import requests
import base64
import io
import aiohttp
import utils

from discord.opus import Encoder as OpusEncoder


from discord.ext import commands

class Song(object):
    folder = 'downloads/'
    
    def __init__(self, yt_obj : pytube.YouTube):
        self.title = yt_obj.title
        self.url = yt_obj.watch_url
        self.video_id = yt_obj.video_id
        self.yt_obj = yt_obj
        self.length = yt_obj.length
        self.current_time = 0

    def __repr__(self):
        return self.title

    def location(self):
        string = self.folder
        string += self.video_id
        string += ".mp3"
        return string

    def is_downloaded(self):
        return os.path.exists(self.location())

    def download(self):
        if not self.is_downloaded():
            MilesYoutube.download_from_pytube(self.yt_obj)

    def kill(self):
        # if too many files are being downloaded not called currently
        os.remove(self.location())

class PlaylistObj(object):
    def __init__(self, yt_obj):
        self.song_list = [Song(x) for x in yt_obj.videos]

    def get_song_list(self):
        return self.song_list


class Player(object):

    def __init__(self, channel):
        self.que = []
        self.isPlaying = False
        self.channel = channel
        self.length = 0

    def queue(self, song:Song):
        self.que.append(song)
        self.length += 1

    def queue_list(self, songs):
        for song in songs:
            self.queue(song)

    def dequeue(self):

        if not self.que:
            return None
        else:
            ret = self.que.pop(0)
            self.length -= 1
            return ret
    def insert(self, song, index):
        self.que.insert(index, song)

    def clear(self):
        self.que.clear()
    
    def is_empty(self):
        if self.que:
            return False
        else:
            return True
    def remove(self, index):
        self.length -= 1
        return self.que.pop(index)


    def __repr__(self):
        ret = ""
        for item in self.que:
            ret += item.title
            ret += '\n'
        return ret

class MyAudioSource(discord.AudioSource):

    def __init__(self, song):
        self.song = song
        self.audio = discord.FFmpegPCMAudio(song.location())

    def read(self):
        self.song.current_time += .02
        return self.audio.read()

    def cleanup(self):
        self.audio.cleanup()

    def seek(self, seconds):
        # delete the old audio and make it fresh again
        self.audio.cleanup()
        self.audio = discord.FFmpegPCMAudio(self.song.location())

        # read that amount of time off the front of the file
        self.audio._stdout.read(OpusEncoder.FRAME_SIZE * seconds * 50)
        self.song.current_time = seconds



load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '=')
game = discord.Game("@Miles if I break")

empty_song = None
player = None
VC = None
yt = MilesYoutube.YT()
now_playing = empty_song
looping = False
loop_size = 0
main_ctx = None

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

@client.command(help="adds bot to your current voice channel can also use =j", aliases=['j'])
async def join(ctx):
    global main_ctx
    main_ctx = ctx
    channel = ctx.author.voice.channel
    if channel == None:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Join", "description": "You must be in a voice channel to use this command"}))
        return
    global player
    player = Player(channel)
    global VC
    if VC == None:
        VC = await channel.connect()
    else:
        await VC.move_to(channel)
    await ctx.send(embed=discord.Embed.from_dict({"title": "Join", "description": "Hello"}))
    asyncio.create_task(start_bot_auto_leave())


@client.command(help="bot leaves")
async def leave(ctx):
    try:
        global player
        player.clear()
        player = None
        global now_playing
        now_playing = None
        global looping
        looping = False
        handle_downloads_space()
        global VC
        await VC.disconnect()
        await ctx.send(embed=discord.Embed.from_dict({"title": "Leave", "description": "Goodbye"}))
        VC = None
        
    except:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Leave", "description": "I'm already gone"}))

@client.command(help="displayes queued songscan also use =q", aliases=["q"])
async def queue(ctx):
    if not VC:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Queue", "description": "Must connect bot to a voice channel first using '=join'"}))
        return

    message = ''
    total_durration = 0
    if now_playing != empty_song:
        message += f"Now Playing:\n[{now_playing.title}]({now_playing.url}) {utils.seconds_to_time(int(now_playing.current_time))}/{utils.seconds_to_time(now_playing.length)}\n\n"
    if player.is_empty() and not looping:
        message += "Queue is empty"
    elif looping:
        message += "Up next in loop: \nuse '=sl' to stop looping\n"
        if loop_size == 0:
            for i, song in enumerate(player.que):
                message += f"{i + 1}. [{song.title}]({song.url}) {utils.seconds_to_time(song.length)}\n"
                total_durration += song.length

        else:
            for i in range(loop_size - 1):
                message += f"{i + 1}. [{player.que[i].title}]({player.que[i].url}) {utils.seconds_to_time(player.que[i].length)}\n"
                total_durration += song.length
            
            if loop_size - 1 < player.length:
                message += f"Out of loop:\n"
                for i in range(loop_size -1, player.length):
                    message += f"[{player.que[i].title}]({player.que[i].url}) {utils.seconds_to_time(player.que[i].length)}\n"

        message += f"Durration of loop: {utils.seconds_to_time(total_durration)}"

            
    else:
        message += f"Songs in queue:\n"
        total_durration = 0
        for i, song in enumerate(player.que):
            message += f"{i + 1}. [{song.title}]({song.url}) {utils.seconds_to_time(player.que[i].length)}\n"
            total_durration += song.length
        message += f"Durration of queue: {utils.seconds_to_time(total_durration)}"

    # discord throws error if embed message length > 6000
    if len(message) > 1500:
        message = message[: message.find("\n", 1500)]
        message += f"\nAnd more...\nDurration of queue: {utils.seconds_to_time(total_durration)}"

    e=discord.Embed.from_dict({
        "title":"Queue",
        "description":f"{message}",
        })
    await ctx.send(embed=e)
    

@client.command(help="adds song to queue can also use =p", aliases=["p"])
async def play(ctx, *, arg = None):
    channel = ctx.author.voice.channel
    
    if not VC:
        await join(ctx)

    elif not is_in_channel_with_bot(ctx):
        await ctx.send(embed=discord.Embed.from_dict({"title": "Play", "description": "You are not in the same voice channel"}))
        return

    if arg == None:
        await ctx.send(content="Must supply a song name/url/search terms after the command\n", embed=discord.Embed.from_dict({"title":"Example",
                                                                                                                              "description": "=play low rider"}))
        return

    global player
    yt_obj, idx = yt.find_video(arg)
    if idx == 0:
        song = Song(yt_obj)
        player.queue(song)
        e = discord.Embed.from_dict({"title": "Play",
                "description":f"Added [{song.title}]({song.url}) {utils.seconds_to_time(song.length)}"
                })
    else:
        pl = PlaylistObj(yt_obj)
        songs = pl.get_song_list()
        message = ""
        for s in songs:
            message += f"Added [{s.title}]({s.url}) {utils.seconds_to_time(song.length)}\n"
        if message == "":
            message = "Doesn't work for auto generated playlists like My Mix or song radio. Sorry :("
        player.queue_list(songs)
        if len(message) > 1500:
            message = message[: message.find("\n", 1500)]
            message += "\nAnd more..."
        e = discord.Embed.from_dict({"title": "From Playlist", 
                                     "description": message})
    
    await ctx.send(embed=e)
    if VC.is_playing():
        pass
    else:
        play_next(None)

    


def play_song():
    global now_playing
    now_playing = player.dequeue()
    now_playing.download()
    if VC == None:
        return
    VC.play(MyAudioSource(now_playing), after = play_next)
    # TODO : implement the below instead of the above
    # VC.play(discord.FFmpegPCMAudio(now_playing.location()), after =lambda: client.loop.call_soon_threadsafe(playnext))

def play_next(e):
    global now_playing
    if player == None:
        now_playing = empty_song
        return

    if looping:
        if loop_size == 0:
            player.queue(now_playing)
        else:
            player.insert(now_playing, loop_size - 1)
    
    if VC == None:
        return
    elif VC.is_playing():
        return
    elif player.is_empty():
        now_playing = empty_song
        return
    else:
        now_playing = empty_song
        play_song()


@client.command(help="Loops number of songs from top of queue defaluts to entire queue can also use =l", aliases=["l"])
async def loop(ctx, *, arg = -1):
    if now_playing == empty_song:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Loop", "description": "No songs playing. Can't loop nothing"}))
        return

    global looping
    global loop_size
    looping = True
    if arg <= 0:
        loop_size = 0
        await ctx.send(embed=discord.Embed.from_dict({"title": "Loop", "description": "Now looping entire queue"}))
    elif arg > player.length + 1:
        loop_size = player.length + 1
        await ctx.send(embed=discord.Embed.from_dict({"title": "Loop", "description": "Now looping {player.length + 1} songs"}))
    else:
        loop_size = arg
        await ctx.send(embed=discord.Embed.from_dict({"title": "Loop", "description": f"Now looping {arg} songs"}))

@client.command(help="Turns off looping can also use =sl", aliases=["sl"])
async def stoploop(ctx):
    global looping
    global loop_size
    looping = False
    loop_size = 0
    await ctx.send(embed=discord.Embed.from_dict({"title": "Stop Loop", "description": "Looping stopped"}))

@client.command(help="Pause current song", aliases=["stop"])
async def pause(ctx):
    VC.pause()

@client.command(help="Skip song can also use =s, =next, =n", aliases=["s", "next", "n"])
async def skip(ctx):
    VC.pause()
    if now_playing == None:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Skip", "description": "Nothing to skip"}))
        return
    await ctx.send(embed=discord.Embed.from_dict({"title": "Skip", "description": f"Skipping [{now_playing.title}]({now_playing.url})"}))
    play_next(None)

@client.command(help="Resumes song")
async def resume(ctx):
    VC.resume()

@client.command(help="Clear the queue can also use =c", aliases=["c"])
async def clear(ctx):
    if looping:
        await stoploop(ctx)
    global player
    player.clear()
    await ctx.send(embed=discord.Embed.from_dict({"title": "Clear", "description": "Queue cleared"}))
    

@client.command(help="Removes songs at specified indexes in the queue")
async def remove(ctx, index):
    try:
        idx = int(index)
    except ValueError:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Remove", "description": "Numbers only!"}))
        return

    if (abs(idx) > player.length):
        await ctx.send(embed=discord.Embed.from_dict({"title": "Remove", "description": "Number larger than the queue"}))
        return

    if(idx >= 0):
        song = player.remove(idx - 1)
    else:
        song = player.remove(idx)

    message = f"Removed {i}. [{song.title}]({song.url})\n" + message

    global loop_size
    if loop_size > player.length + 1:
        loop_size = player.length + 1
        
    await ctx.send(embed=discord.Embed.from_dict({"title": "Remove", "description": message}))

def is_in_channel_with_bot(ctx):
    channel = ctx.author.voice.channel
    return channel == VC.channel

async def start_bot_auto_leave():
    # sometimes the VC.channel.members returns with only the bot inside when I am in the call. Unsure why that happens.
    while VC:
        if len(VC.channel.members) <= 1:
            await leave(main_ctx)
            break

        await asyncio.sleep(300)
    return

#region dall-e
@client.command(help="Pass me text and ill give you images back in about a minute. Uses web api of dall-e mini to generate 9 images based on prompt.\nExample usage: =dalle poker house on fire while homeless dance", aliases=["da"])
async def dalle(ctx, *, arg):
    async with aiohttp.ClientSession() as session:
        await ctx.send(embed=discord.Embed.from_dict({"title": "generating images", "description": f"generating images from prompt \"{arg}\".\nThis could take up to 2 minutes."}))
        async with session.post("https://backend.craiyon.com/generate", json={"prompt": arg}) as r:
            resp = await r.json()
            images = resp['images']
            
        # upscaling each image
        tasks = []
        for img in images:
            tasks.append(asyncio.ensure_future(upscale(img, session)))

        upscaled_images = await asyncio.gather(*tasks)

        files = []
        for img in upscaled_images:
            f = discord.File(io.BytesIO(base64.b64decode(img)), filename=f"{arg}.jpeg")
            files.append(f)

        await ctx.send(files=files)
        
async def upscale(image_bytes, session):
    data_string = "data:image//JPEG;base64,"
    async with session.post("https://upscaler.zyro.com/v1/ai/image-upscaler", json={"image_data": f"{data_string}{image_bytes}"}) as r:
        resp = await r.json()
        return resp["upscaled"][len(data_string) - 1:]

#endregion
#region MTG
Offers = ["Draw three cards.",
          "Conjure a Manor Guardian card into your hand.",
          "Return two random creature cards from your graveyard to your hand. They perpetually gain +1/+1.",
          "Return a random creature card with the highest mana value from among cards in your graveyard to the battlefield.",
          "You get an emblem with \"Creatures you control get +2/+0.\"",
          "You get an emblem with \"Spells you cast cost {B} less to cast.\"",
          "You get an emblem with \"Davriel planeswalkers you control have '+2: Draw a card.'\"",
          "You get an emblem with \"Whenever you draw a card, you gain 2 life.\""]

Conditions = ["You lose 6 life.",
              "Exile two cards from your hand. If fewer than two cards were exiled this way, each opponent draws cards equal to the difference.",
              "Sacrifice two permanents.",
              "Each creature you don't control perpetually gains +1/+1.",
              "You get an emblem with \"Creatures you control get -1/-0.\"",
              "You get an emblem with \"Spells you cast cost one black mana more to cast.\"",
              "You get an emblem with \"Whenever you draw a card, exile the top two cards of your library.\"",
              "You get an emblem with \"At the beginning of your upkeep, you lose 1 life for each creature you control.\""]

@client.command(help="Davriel Crane Contract and Contitions. Ten seconds between offer and conditions. Choose quickly", aliases=["d"])
async def davriel(ctx):
    offer1, offer2, offer3 = random.sample(range(0,8),3)
    cond1, cond2, cond3 = random.sample(range(0,8),3)

    await ctx.send(embed=discord.Embed.from_dict({"title": "Offers", "description": f"Choose one offer.\n\n||1.\t{Offers[offer1]}\n2.\t{Offers[offer2]}\n3.\t{Offers[offer3]}||"}))

    await ctx.send(embed=discord.Embed.from_dict({"title": "Conditions", "description": f"Choose one Condition.\n\n||1.\t{Conditions[cond1]}\n2.\t{Conditions[cond2]}\n3.\t{Conditions[cond3]}||"}))

#endregion


@client.command(help="seeks to time in current track", aliases=["jump"] )
async def seek(ctx, time):
    converted_time = utils.time_to_seconds(time)
    if converted_time < 0:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Seek", "description": "Provide a valid time format, format of minutes:seconds or only seconds\nFor example: =seek 150 or =seek 2:30"}))
        return

    if converted_time > now_playing.length:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Seek", "description": "Time specified is longer than current song's durration"}))
        return

    VC.pause()
    VC.source.seek(converted_time)
    VC.resume()
    await ctx.send(embed=discord.Embed.from_dict({"title": "Seek", "description": f"Playing [{now_playing.title}]({now_playing.url}) {utils.seconds_to_time(int(now_playing.current_time))}/{utils.seconds_to_time(now_playing.length)}"}))
    return

@client.command(help="skips the given amount of time in current track", aliases=["ff"] )
async def fastforward(ctx, time):
    converted_time = utils.time_to_seconds(time)
    if converted_time < 0:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Fast Forward", "description": "Provide a valid time format, format of minutes:seconds or only seconds\nFor example: =seek 150 or =seek 2:30"}))
        return
    
    seek_time = int(converted_time + now_playing.current_time)
    if seek_time > now_playing.length:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Seek", "description": "Time specified is longer than current song's durration"}))
        return
    
    VC.pause()
    VC.source.seek(seek_time)
    VC.resume()
    await ctx.send(embed=discord.Embed.from_dict({"title": "Fast Forward", "description": f"Playing [{now_playing.title}]({now_playing.url}) {utils.seconds_to_time(int(now_playing.current_time))}/{utils.seconds_to_time(now_playing.length)}"}))
    return



client.run(token)


