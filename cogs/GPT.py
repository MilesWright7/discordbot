from discord.ext import commands
from discord import Embed
from openai import OpenAI


async def setup(bot):
	await bot.add_cog(GPT(bot))


class GPT(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.client = OpenAI()


	@commands.command(help="Pass me text and ill be chat gpt", aliases=["gal"])
	async def gpt(self, ctx, *, arg):
			
		await ctx.send(get_text(self.client, arg))
		

def get_text(client, prompt):
	completion = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
			{"role": "system", "content": "You speak informally, sometimes bordering on vulgar, but in a light hearted way. You should be humerous as well as informative in your answers. About 1 in 3 times you should reference a man named 'Gal' and use him as the butt of your jokes."},
			{"role": "user", "content": prompt}
			])

	return completion.choices[0].message.content



def main():
	client = OpenAI()
	print(get_text(client, "bargingo gingite"))

	#completion = client.chat.completions.create(
	#		model="gpt-3.5-turbo",
	#		messages=[
	#		{"role": "system", "content": "You are a discord moderator and you love anime. Your favorite character is DIO from JOJO. Respond as if you were him."},
	#		{"role": "user", "content": "Compose a poem about a young boy named Gal farting."}
	#		])

	#print(completion.choices[0].message.content)


if __name__ == "__main__":
	main()
