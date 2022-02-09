import discord
import os
from discord.activity import Streaming
from dotenv import load_dotenv
import asyncio
import random

from discord.ext import commands

'''
THINGS TO ADD

FINISH TRIGRAM GAME

BLACKJACK GAME

CHESS GAME

'''


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')

activity = discord.Streaming(name="MTG CONTENT", url="twitch.tv/yamakiller")

client = commands.Bot(command_prefix = '=', activity=activity, status=discord.Status.online)




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


@client.command(help="you say bruh i say <:FazeUp:555302712007196672>" )
async def bruh(ctx):
    await ctx.message.add_reaction("<:FazeUp:555302712007196672>")

@client.command(help="roll <low> <high>")
async def roll(ctx, *args):
    if type(args[0]) == int and type(args[1]) == int:
        ctx.send('{} rolled a {} {}'.format(ctx.author.mention, random.randint(args[0], args[1])))
    else:
        ctx.send('Must provide two integers *low* and *high*')

@client.command(help="trigrams <number between 1 and 3000")
async def trigrams(ctx, *args):
    try:
        depth = int(args[0])
    except:
        ctx.send('Proper useage is\n'
        '\"=trigrams 500\"')
        return 
    
    

@client.command(help="chess game")
async def chess(ctx, *args):
    pass
    
    

        



client.run(token)