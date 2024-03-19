from discord.ext import commands
from discord import Embed
from openai import OpenAI


async def setup(bot):
	await bot.add_cog(Dalle(bot))


class Dalle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.client = OpenAI()


	@commands.command(help="Pass me text and ill give you images. Using dalle-2", aliases=["da"])
	async def dalle(self, ctx, *, arg):
		await ctx.send(embed=Embed.from_dict({"title": "generating images", "description": f"generating images from prompt \"{arg}\".\nThis could take a bit."}))
			
		await ctx.send(get_images(self.client, arg))
		
	@commands.command(help="Pass me text and ill give you images. Using dalle-3", aliases=["da3"])
	async def dalle3(self, ctx, *, arg):
		await ctx.send(embed=Embed.from_dict({"title": "generating images", "description": f"generating images from prompt \"{arg}\".\nThis could take a bit."}))
			
		await ctx.send(get_images_improved(self.client, arg))

def get_images(client, prompt):
	response = client.images.generate(
		model="dall-e-2",
		prompt=prompt,
		size="1024x1024",
		quality="standard",
		n=1,
		)


	return response.data[0].url

def get_images_improved(client, prompt):
	response = client.images.generate(
		model="dall-e-3",
		prompt=prompt,
		size="1024x1024",
		quality="standard",
		n=1,
		)


	return response.data[0].url


def main():
	client = OpenAI()
	print(get_images(client, "farting doggy"))

	#completion = client.chat.completions.create(
	#		model="gpt-3.5-turbo",
	#		messages=[
	#		{"role": "system", "content": "You are a discord moderator and you love anime. Your favorite character is DIO from JOJO. Respond as if you were him."},
	#		{"role": "user", "content": "Compose a poem about a young boy named Gal farting."}
	#		])

	#print(completion.choices[0].message.content)


if __name__ == "__main__":
	main()
