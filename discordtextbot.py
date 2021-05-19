import discord
import os
from discord.activity import Streaming
from dotenv import load_dotenv
import asyncio
import random

from discord.ext import commands




load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')
client = commands.Bot(command_prefix = '=')

game = discord.Game("pizza time")



# for trigram game
trigram_set = set()
with open('./assets/words_alpha_trigram_sorted.txt', 'r') as f:
    for line in f:
        key, value = line.split(' ')
        trigram_set.add((key, value))

with open('./assets/words_alpha.txt', 'r') as f:
    words = set(line[:-1] for line in f)



@client.event
async def on_ready():
    server =  discord.utils.get(client.guilds, name=guild)
    print(f'{client.user} has connected to Discord!\n'
          f'{server.name}(id: {server.id})')
    await client.change_presence(status=discord.Status.online, activity=Streaming("yamakiller", "twitch.tv/yamakiller", game="MaGiC ThE GaThErInG",));


@client.command(help="you say bruh i say <:FazeUp:555302712007196672>" )
async def bruh(ctx):
    await ctx.message.add_reaction("<:FazeUp:555302712007196672>")

@client.command(help="roll <low> <high>")
async def roll(ctx, *args):
    if type(args[0]) == int and type(args[1]) == int:
        ctx.send('{} rolled a {} {}'.format(ctx.author.mention, random.randint(args[0], args[1])))
    else:
        ctx.send('Must provide two integers *low* and *high*')

@client.command(help="")
async def trigrams(ctx, *args):
    try:
        depth = int(args[0])
    except:
        ctx.send('Proper useage is for example\n'
        '\"=trigrams 500\"')
        return 1
    
    

        



client.run(token)