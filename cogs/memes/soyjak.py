import discord
from discord.ext import commands
from discord.utils import MISSING
from discord import app_commands

from PIL import Image
from io import BytesIO

from utils import handle_errors, edit_image, no_ping
from cogs.general.gif import GifizeView


soyjak_point = Image.open("assets/memes/soyjak_point.png").convert("RGBA")


class SoyjakCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["ыщнофл", "сойджак"],
		description="Вставляет на изображение удивленных сойджаков",
		usage="`/soyjak <изображение>`",
		help="### Пример:\n`/soyjak image.png`"
	)
	@app_commands.default_permissions(discord.Permissions(administrator=True))

	async def soyjak(self, ctx: commands.Context, image: discord.Attachment):
		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		extension = image.filename.split(".")[-1]

		soyjaked = edit_image(
			Image.open(BytesIO(await image.read())),
			extension,
			soyjak
		)
		soyjaked_discorded = discord.File(soyjaked, filename=image.filename)
		await ctx.reply(
			file=soyjaked_discorded,
			view=GifizeView() if extension != "gif" else MISSING,
			allowed_mentions=no_ping
		)

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
