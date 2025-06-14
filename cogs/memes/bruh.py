import discord
from discord.ext import commands

from PIL import Image
from io import BytesIO
from utils import handle_errors, ImageText, edit_image



class BruhCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["druh", "брух", "икгр", "брах"],
		description="Добавляет текст на изображение",
		usage="`/bruh <изображение> <текст>",
		help="### Пример:\n`/bruh` `image.png` `Пей горн`"
	)

	async def bruh(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		*,
		text
	):
		if "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		bruhed = edit_image(
			Image.open(BytesIO(await image.read())),
			image.content_type.split("/")[-1],
			bruh,
			text=text
		)
		bruhed_discorded = discord.File(bruhed, filename=image.filename)
		await ctx.send(file=bruhed_discorded)

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

