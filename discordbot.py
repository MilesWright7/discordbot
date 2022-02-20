import discord
import os
from dotenv import load_dotenv
import MilesYoutube
import asyncio
import random
from SpaceManagement import handle_downloads_space

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

    def kill(self):
        # if too many files are being downloaded not called currently
        os.remove(self.location)


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
    def insert(self, song, index):
        self.que.insert(index, song)

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
looping = False
loop_size = 0

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
    channel = ctx.author.voice.channel
    global player
    player = Player(channel)
    global VC
    VC = await channel.connect()
    await start_bot_auto_leave()


@client.command(help="bot leaves")
async def leave(ctx):
    try:
        global VC
        await VC.disconnect()
        VC = None
        global player
        player = None
        handle_downloads_space()
        
    except:
        await ctx.send("Not in voice channel")

@client.command(help="displayes queued songscan also use 'q'", aliases=["q"])
async def queue(ctx):
    if not VC:
        await ctx.send("Must connect bot to a voice channel first using '=join'")
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
        "title":f"Queue",
        "description":f"{message}",
        })
    await ctx.send(embed=e)
    

@client.command(help="adds song to queue can also use '=p'", aliases=["p"])
async def play(ctx, *, arg = None):
    channel = ctx.author.voice.channel
    
    if not is_in_channel_with_bot(ctx):
        await ctx.send("You are not in the same voice channel")
        return

    if not VC:
        await ctx.send("Must connect bot to a voice channel first using \"join\"")
        return

    if arg == None:
        await ctx.send(content="Must supply a song name/url/search terms after the command\n", embed=discord.Embed.from_dict({"title":"Example",
                                                                                                                              "description": "=play low rider"}))
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
        return
    else:
        now_playing = empty_song
        play_song()


@client.command(help="Loops number of songs from top of queue defaluts to entire queue can also use '=l'", aliases=["l"])
async def loop(ctx, *, arg = -1):
    if now_playing == empty_song:
        await ctx.send("No songs playing. Can't loop nothing")
        return

    global looping
    global loop_size
    looping = True
    if arg <= 0:
        loop_size = 0
        await ctx.send("Now looping entire queue")
    elif arg > player.length + 1:
        loop_size = player.length + 1
        await ctx.send("Now looping {player.length + 1} songs")
    else:
        loop_size = arg
        await ctx.send(f"Now looping {arg} songs")

@client.command(help="Turns off looping can also use '=sl'", aliases=["sl"])
async def stoploop(ctx):
    global looping
    global loop_size
    looping = False
    loop_size = 0
    await ctx.send("Looping stopped")

@client.command(help="Pause current song")
async def pause(ctx):
    VC.pause()

@client.command(help="Stop playing")
async def stop(ctx):
    VC.stop()

@client.command(help="Skip song can also use '=s'", aliases=["s"])
async def skip(ctx):
    VC.stop()
    if looping:
        await stoploop(ctx)
    await ctx.send(f"Skipping {now_playing.title}")
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
    

def is_in_channel_with_bot(ctx):
    channel = ctx.author.voice.channel
    return channel == VC.channel

async def start_bot_auto_leave():
    # sometimes the VC.channel.members returns with only the bot inside when I am in the call. Unsure why that happens.
    while VC:
        if len(VC.channel.members) <= 1:
            await leave(None)
            break

        await asyncio.sleep(300)
    return


client.run(token)


