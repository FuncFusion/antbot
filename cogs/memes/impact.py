import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from PIL import Image
from io import BytesIO

from utils import handle_errors, ImageText, edit_image, closest_match, no_ping
from cogs.general.gif import GifizeView

positions = [app_commands.Choice(name="Верх", value="up"), app_commands.Choice(name="Низ", value="down")]
positions_aliases = {
	"up": ["верх", "в"],
	"down": ["низ", "н"]
}


class ImpactCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["шьзфсе", "импакт", "геншин"],
		description="Добавляет текст на изображение",
		usage="`/impact <изображение> <текст> <позиция>`",
		help="### Пример:\n`/impact image.png пей горн Низ`"
	)

	async def impact(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		text: str,
		position: str="down"
	):
		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		extension = image.filename.split(".")[-1]

		position = closest_match(position, positions_aliases)
		impacted = edit_image(
			Image.open(BytesIO(await image.read())),
			extension,
			impact,
			text=text,
			position=position
		)
		impacted_discorded = discord.File(impacted, filename=image.filename)
		await ctx.reply(
			file=impacted_discorded, 
			view=GifizeView() if extension != "gif" else MISSING,
			allowed_mentions=no_ping
		)
	
	@impact.autocomplete(name="position")
	async def position_default_choices(self, ctx, curr):
		return positions

	@impact.error
	async def impact_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])


def impact(image: Image.Image, text: str, position: str):
	font = "assets/memes/impact.ttf"
	size = int(image.width/10)
	color = (255, 255, 255)
	width = image.size[0]
	height = image.size[1]
	
	image = image.convert(mode="RGBA")
	
	# Calculate required heights first
	impact_text = ImageText(image, anchor="ma")
	padding = int(height/12)

	# if (taken_space:=impact_text.get_height((int(width/2), 0), text, width, font, size)) > (free_space:=image.height - padding*2):
	# 	size = (size / taken_space) * free_space
	while impact_text.get_height(
		(int(width/2), 0), text, width, font, size, stroke_width=int(size/16), stroke_fill=(0, 0, 0, 255)
	) > image.height / 3 and size > 11:
		size -= 10

	if position == "down":
		text_height = impact_text.get_height(
			(int(width/2), 0), 
			text, 
			width, 
			font, 
			size, 
			stroke_width=int(size/16), 
			stroke_fill=(0, 0, 0, 255)
		)
		padding = height - padding - text_height
	
	impact_text.write_text_box(
		(int(width/2), padding), 
		text, 
		width, 
		font, 
		size, 
		color, 
		stroke_width=int(size/16), 
		stroke_fill=(0, 0, 0, 255)
	)
	
	return image

