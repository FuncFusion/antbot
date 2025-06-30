import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from PIL import Image
from io import BytesIO

from utils import handle_errors, ImageText, edit_image, no_ping
from cogs.general.gif import GifizeView


class ImpactCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["шьзфсе", "импакт", "геншин"],
		description="Добавляет текст на изображение",
		usage="`/impact <изображение> <текст> <позиция>`",
		help="### Пример:\n`/impact image.png пей горн Низ`"
	)
	@app_commands.describe(
		top_text="Верхний текст (до 500 символов)",
		bottom_text="Нижний текст (до 500 символов)"
	)
	@app_commands.default_permissions(discord.Permissions.administrator)

	async def impact(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		top_text: str="",
		bottom_text: str=""
	):
		top_text = top_text[:500]
		bottom_text = bottom_text[:500]

		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		extension = image.filename.split(".")[-1]

		impacted = edit_image(
			Image.open(BytesIO(await image.read())),
			extension,
			impact,
			top_text=top_text,
			bottom_text=bottom_text
		)
		impacted_discorded = discord.File(impacted, filename=image.filename)
		await ctx.reply(
			file=impacted_discorded, 
			view=GifizeView() if extension != "gif" else MISSING,
			allowed_mentions=no_ping
		)

	@impact.error
	async def impact_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])


def impact(image: Image.Image, top_text: str, bottom_text: str):
	font = "assets/memes/impact.ttf"
	get_size = lambda text: int((((image.width+image.height)/2)/10) / max(1, (len(text)/25)*0.5))
	top_size = get_size(top_text)
	bottom_size = get_size(bottom_text)
	color = (255, 255, 255)
	width = image.size[0]
	height = image.size[1]
	padding = int(height/16)
	text_width = width - padding
	
	image = image.convert(mode="RGBA")
	
	# Calculate required heights first
	impact_text = ImageText(image, anchor="ma")

	if bottom_text != "":
		text_height = impact_text.get_height(
			(int(width/2), 0), bottom_text, 
			text_width, font, bottom_size,
			stroke_width=int(bottom_size/16), 
			stroke_fill=(0, 0, 0, 255)
		)
		y = height - padding - text_height
		impact_text.write_text_box(
			(int(width/2), y), bottom_text, 
			text_width, font, bottom_size, color, 
			stroke_width=int(bottom_size/16), 
			stroke_fill=(0, 0, 0, 255)
		)
	
	if top_text != "":
		impact_text.write_text_box(
		(int(width/2), padding), top_text, 
		text_width, font, top_size, color, 
		stroke_width=int(top_size/16), 
		stroke_fill=(0, 0, 0, 255)
	)
	
	return image

