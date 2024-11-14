from discord.ext import commands
from discord import Embed


async def setup(bot):
	await bot.add_cog(Sync(bot))


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    def check_if_it_is_me(ctx):
        return ctx.message.author.id == 218920440297553920

    @commands.command(help="dont use this")
    @commands.check(check_if_it_is_me)
    async def sync(self, ctx):
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands globally")
        return