import discord
from discord.ext import commands
from discord.app_commands import Choice

from PIL import Image
from io import BytesIO
from utils import handle_errors, ImageText, edit_image, closest_match

positions = [Choice(name="Верх", value="up"), Choice(name="Низ", value="down")]
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
		if "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()

		position = closest_match(position, positions_aliases)
		impacted = edit_image(
			Image.open(BytesIO(await image.read())),
			image.content_type.split("/")[-1],
			impact,
			text=text,
			position=position
		)
		impacted_discorded = discord.File(impacted, filename=image.filename)
		await ctx.send(file=impacted_discorded)
	
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
	size = int(max(image.size)/8)
	color = (255, 255, 255)
	width = image.size[0]
	height = image.size[1]
	
	image = image.convert(mode="RGBA")
	
	# Calculate required heights first
	impact_text = ImageText(image, anchor="ma", stroke_width=int(size/16), stroke_fill=(0, 0, 0, 255))
	y = int(height/12)

	if position == "down":
		text_height = impact_text.get_height((int(width/2), 0), text, width, font, size)
		y = height - y - text_height
	
	impact_text.write_text_box((int(width/2), y), text, width, font, size, color)
	
	return image

