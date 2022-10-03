from discord.ext import commands
from discord import Embed
import random


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


def setup(bot):
	bot.add_cog(MTG(bot))


class MTG(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	@commands.command(help="Davriel Crane Contract and Contitions. Ten seconds between offer and conditions. Choose quickly", aliases=["d"])
	async def davriel(self, ctx):
		offer1, offer2, offer3 = random.sample(range(0,8),3)
		cond1, cond2, cond3 = random.sample(range(0,8),3)

		await ctx.send(embed=Embed.from_dict({"title": "Offers", "description": f"Choose one offer.\n\n||1.\t{Offers[offer1]}\n2.\t{Offers[offer2]}\n3.\t{Offers[offer3]}||"}))

		await ctx.send(embed=Embed.from_dict({"title": "Conditions", "description": f"Choose one Condition.\n\n||1.\t{Conditions[cond1]}\n2.\t{Conditions[cond2]}\n3.\t{Conditions[cond3]}||"}))