import discord
import os
from dotenv import load_dotenv
import pytube
from pytube.contrib.playlist import Playlist
import MilesYoutube
import asyncio
import random
from SpaceManagement import handle_downloads_space

from discord.ext import commands

class Song(object):
    folder = 'downloads/'
    
    def __init__(self, yt_obj : pytube.YouTube):
        self.title = yt_obj.title
        self.url = yt_obj.watch_url
        self.video_id = yt_obj.video_id
        self.yt_obj = yt_obj

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

    def queue_list(self, songs: [Song]):
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

@client.command(help="adds bot to your current voice channel can also use '=j'", aliases=['j'])
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
    await start_bot_auto_leave()


@client.command(help="bot leaves")
async def leave(ctx):
    try:
        global VC
        await VC.disconnect()
        await ctx.send(embed=discord.Embed.from_dict({"title": "Leave", "description": "Goodbye"}))
        VC = None
        global player
        player = None
        global now_playing
        now_playing = None
        global looping
        looping = False
        handle_downloads_space()
        
    except:
        await ctx.send("Not in voice channel")

@client.command(help="displayes queued songscan also use 'q'", aliases=["q"])
async def queue(ctx):
    if not VC:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Queue", "description": "Must connect bot to a voice channel first using '=join'"}))
    message = ''
    if now_playing != empty_song:
        message += f"Now Playing:\n[{now_playing.title}]({now_playing.url})\n\n"
    if player.is_empty() and not looping:
        message += "Queue is empty"
    elif looping:
        message += "Up next in loop: \nuse '=sl' to stop looping\n"
        if loop_size == 0:
            for i, song in enumerate(player.que):
                message += f"{i + 1}. [{song.title}]({song.url})\n"

        else:
            for i in range(loop_size - 1):
                message += f"{i + 1}. [{player.que[i].title}]({player.que[i].url})\n"
            
            if loop_size - 1 < player.length:
                message += f"Out of loop:\n"
                for i in range(loop_size -1, player.length):
                    message += f"[{player.que[i].title}]({player.que[i].url})\n"

            
    else:
        message += f"Songs in queue:\n"
        for i, song in enumerate(player.que):
            message += f"{i + 1}. [{song.title}]({song.url})\n"

    e=discord.Embed.from_dict({
        "title":"Queue",
        "description":f"{message}",
        })
    await ctx.send(embed=e)
    

@client.command(help="adds song to queue can also use '=p'", aliases=["p"])
async def play(ctx, *, arg = None):
    channel = ctx.author.voice.channel
    
    if not is_in_channel_with_bot(ctx):
        await ctx.send(embed=discord.Embed.from_dict({"title": "Play", "description": "You are not in the same voice channel"}))
        return

    if not VC:
        await ctx.send(embed=discord.Embed.from_dict({"title": "Play", "description": "Must connect bot to a voice channel first using \"join\""}))
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
                "description":f"Added [{song.title}]({song.url}) to queue"
                })
    else:
        pl = PlaylistObj(yt_obj)
        songs = pl.get_song_list()
        message = ""
        for s in songs:
            message += f"Added [{s.title}]({s.url}) to queue\n"
        if message == "":
            message = "Doesn't work for auto generated playlists like My Mix or song radio. Sorry :("
        player.queue_list(songs)
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
    VC.play(discord.FFmpegPCMAudio(now_playing.location()), after = play_next)
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


@client.command(help="Loops number of songs from top of queue defaluts to entire queue can also use '=l'", aliases=["l"])
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

@client.command(help="Turns off looping can also use '=sl'", aliases=["sl"])
async def stoploop(ctx):
    global looping
    global loop_size
    looping = False
    loop_size = 0
    await ctx.send(embed=discord.Embed.from_dict({"title": "Stop Loop", "description": "Looping stopped"}))

@client.command(help="Pause current song", aliases=["stop"])
async def pause(ctx):
    VC.pause()

@client.command(help="Skip song can also use '=s'", aliases=["s"])
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

@client.command(help="Clear the queue can also use '=c'", aliases=["c"])
async def clear(ctx):
    if looping:
        await stoploop(ctx)
    global player
    player.clear()
    await ctx.send(embed=discord.Embed.from_dict({"title": "Clear", "description": "Queue cleared"}))
    

@client.command(help="Removes songs at specified indexes in the queue")
async def remove(ctx, *, args):
    int_args = []
    for arg in args.split(" "):
        try:
            int_args.append(int(arg))

        except ValueError:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Remove", "description": "Numbers only!"}))

    int_args.sort(reverse=True)
    for i in int_args:
        if i > player.length or i < 1:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Remove", "description": "A number is out of the queue's range"}))

    message = ""
    for i in int_args:
        song = player.remove(i-1)
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




client.run(token)


