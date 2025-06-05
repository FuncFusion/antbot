import discord
from discord.ext import commands

from PIL import Image
from io import BytesIO

from utils import handle_errors, edit_image


soyjak_point = Image.open("assets/memes/soyjak_point.png").convert("RGBA")


class SoyjakCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["ыщнофл", "сойджак"],
		description="Вставляет на изображение удивленных сойджаков",
		usage="`/soyjak <изображение>`",
		help="### Пример:\n`/soyjak image.png`"
	)

	async def soyjak(self, ctx: commands.Context, image: discord.Attachment):
		if "image" not in image.content_type:
			raise Exception("Not image")
		soyjaked = edit_image(
			Image.open(BytesIO(await image.read())),
			image.content_type.split("/")[-1],
			soyjak
		)
		soyjaked_discorded = discord.File(soyjaked, filename=image.filename)
		await ctx.send(file=soyjaked_discorded)

	@soyjak.error
	async def soyjak_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])


def soyjak(image: Image.Image):
	# image.resize((452, 332))
	image = image.convert("RGBA")
	# paste 30 24
	image = image.crop(
		(
			-(image.width*0.25), -(image.height*0.35),
			image.width + (image.width*0.25), image.height + (image.height*0.5)
		)
	)
	resized_sjp = soyjak_point.resize(image.size)
	image.paste(resized_sjp, (0,0), resized_sjp)
	return image
