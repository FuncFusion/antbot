import discord
from discord.ext import commands
from discord.utils import MISSING
from discord import app_commands

from PIL import Image
from io import BytesIO

from utils import handle_errors, ImageText, edit_image, no_ping
from cogs.general.gif import GifizeView


class BruhCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["druh", "брух", "икгр", "брах"],
		description="Добавляет текст на изображение",
		usage="`/bruh <изображение> <текст>",
		help="### Пример:\n`/bruh` `image.png` `Пей горн`"
	)
	@app_commands.default_permissions(discord.Permissions.administrator)

	async def bruh(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		*,
		text: str
	):
		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		extension = image.filename.split(".")[-1]

		bruhed = edit_image(
			Image.open(BytesIO(await image.read())),
			extension,
			bruh,
			text=text
		)
		bruhed_discorded = discord.File(bruhed, filename=image.filename)
		await ctx.reply(
			file=bruhed_discorded,
			view=GifizeView() if extension != "gif" else MISSING,
			allowed_mentions=no_ping
		)

	@bruh.error
	async def bruh_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])



def bruh(image: Image.Image, text):
	font = "assets/memes/noto_bold.ttf"
	size = int(max(image.size)/8)
	color = (0, 0, 0)
	width = image.size[0]
	
	image = image.convert(mode="RGBA")
	text_part = Image.new("RGBA", (width, 16), (255, 255, 255))
	
	# Calculate required heights first
	bruh_text = ImageText(text_part, anchor="ma")
	text_height = bruh_text.get_height((int(width/2), 16), text, width, font, size)
	
	# Resize the text
	text_part = text_part.resize((width, text_height + 48))
	bruh_text = ImageText(text_part, anchor="ma")
	bruh_text.write_text_box((int(width/2), 16), text, width, font, size, color)

	canvas = Image.new("RGBA", (width, text_part.size[1] + image.size[1]))
	canvas.paste(text_part, (0,0))
	canvas.paste(image, (0, text_part.size[1]))
	
	return canvas

