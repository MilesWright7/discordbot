from discord.ext import commands
from discord import Embed, File
import asyncio
import aiohttp
import base64
import io


def setup(bot):
	bot.add_cog(Dalle(bot))


class Dalle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(help="Pass me text and ill give you images back in about a minute. Uses web api of dall-e mini to generate 9 images based on prompt.\nExample usage: =dalle poker house on fire while homeless dance", aliases=["da"])
	async def dalle(self, ctx, *, arg):
		async with aiohttp.ClientSession() as session:
			await ctx.send(embed=Embed.from_dict({"title": "generating images", "description": f"generating images from prompt \"{arg}\".\nThis could take up to 2 minutes."}))
			async with session.post("https://backend.craiyon.com/generate", json={"prompt": arg}) as r:
				resp = await r.json()
				images = resp['images']
			
			# upscaling each image
			tasks = []
			for img in images:
				tasks.append(asyncio.ensure_future(self.upscale(img, session)))

			upscaled_images = await asyncio.gather(*tasks)

			files = []
			for img in upscaled_images:
				f = File(io.BytesIO(base64.b64decode(img)), filename=f"{arg}.jpeg")
				files.append(f)

			await ctx.send(files=files)
		

	@staticmethod
	async def upscale(image_bytes, session):
		data_string = "data:image//JPEG;base64,"
		async with session.post("https://upscaler.zyro.com/v1/ai/image-upscaler", json={"image_data": f"{data_string}{image_bytes}"}) as r:
			resp = await r.json()
			return resp["upscaled"][len(data_string) - 1:]