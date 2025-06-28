import discord
from discord.ext import commands

from PIL import Image
from io import BytesIO

from utils import handle_errors, ImageText, edit_image



class DemotivatorCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["вуьщешмфещк", "демотиватор", "дем", "dem"],
		description="Вставляет изображение в черную рамку с текстом",
		usage="`/demotivator <изображение> <большой текст> [маленький текст]`",
		help="### Пример:\n`/demotivator` `image.png` `SAY GEX` `pay gorn`"
	)

	async def demotivator(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		title: str="",
		description: str=""
	):
		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		demotivated = edit_image(
			Image.open(BytesIO(await image.read())),
			image.filename.split(".")[-1],
			demotivator,
			huge_text=title,
			normal_text=description
		)
		demotivated_discorded = discord.File(demotivated, filename=image.filename)
		await ctx.send(file=demotivated_discorded)

	@demotivator.error
	async def demotivator_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])



base_demotivator = Image.open("assets/memes/demotivator.png").convert(mode="RGBA")

def demotivator(image, huge_text, normal_text):
	normal_font = "assets/memes/arial.ttf"
	huge_font = "assets/memes/times.ttf"
	huge_size = 36
	normal_size = 15
	color = (255, 255, 255)
	
	image = image.convert(mode="RGBA").resize((450, 330))
	demotivator = base_demotivator.copy()  # Make a copy to avoid modifying original
	demotivator.paste(image, (31, 25))
	
	# Calculate required heights first
	demotivator_text = ImageText(demotivator, anchor="ma")
	huge_y = 370
	huge_text_height = demotivator_text.get_height((256, huge_y), huge_text, 480, huge_font, huge_size)
	normal_y = huge_y + huge_text_height + 7
	normal_text_height = demotivator_text.get_height((256, normal_y), normal_text, 400, normal_font, normal_size)
	
	# Calculate total required height
	total_required_height = normal_y + normal_text_height + 15
	
	# Resize the image once if needed
	if total_required_height > demotivator.size[1]:
		new_height = int(total_required_height)
		# Create new image with black background
		resized_demotivator = Image.new('RGBA', (demotivator.size[0], new_height), (0, 0, 0, 255))
		resized_demotivator.paste(demotivator, (0, 0))
		demotivator = resized_demotivator
		demotivator_text = ImageText(demotivator, anchor="ma")
	
	# Draw both texts on the properly sized image
	draw = demotivator_text.draw
	draw.ink = 0
	draw.fill = True
	
	# Drawing huge text
	demotivator_text.write_text_box((256, huge_y), huge_text, 480, huge_font, huge_size, color)
	
	# Drawing normal text
	demotivator_text.write_text_box((256, normal_y), normal_text, 400, normal_font, normal_size, color)
	
	return demotivator
