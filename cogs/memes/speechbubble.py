import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from PIL import Image
import numpy as np
from io import BytesIO

from utils import handle_errors, edit_image, closest_match, no_ping
from cogs.general.gif import GifizeView

transparent_aliases = {
	"True": ["T", "t", "yes", "y", "1", "да", "д", "прозрачный"],
	"False": ["F", "f", "no", "n", "0", "нет", "н", "непрозрачный"]
}
direction_aliases = {
	"left": ["l", "лево", "л"],
	"right": ["r", "право", "п"],
	"center": ["c", "центр", "ц"]
}
position_aliases = {
	"up" : ["u", "в", "верх"],
	"down": ["d", "н", "низ"]
}
transparents = [app_commands.Choice(name="Прозрачный", value="True"), app_commands.Choice(name="Непрозрачный", value="False")]
directions = [app_commands.Choice(name="Лево", value="left"), app_commands.Choice(name="Право", value="right"), app_commands.Choice(name="Центр", value="center")]
positions = [app_commands.Choice(name="Верх", value="up"), app_commands.Choice(name="Низ", value="down")]


class SpeechbubbleCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["ызуусригииду", "спичбабл", "спичбаббл", "сб", "sb"],
		description="💬",
		usage="`/speechbubble <изображение> [Прозрачность спичбаббла] "
			"[Положение стрелки спичбаббла] [Положение первого спичбаббла] "
			"[Прозрачность второго спичбаббла] [Положение стрелки второго спичбаббла]`",
		help="### Пример:\n`/speechbubble image.png Прозрачный Право Непрозрачный Лево`"
	)
	@app_commands.describe(
		transparent="Прозрачность спичбаббла",
		direction="Положение стрелки спичбаббла",
		position="Положение первого спичбаббла",
		transparent2="Прозрачность второго спичбаббла",
		direction2="Положение стрелки второго спичбаббла",
	)
	@app_commands.default_permissions(discord.Permissions(administrator=True)

	async def speechbubble(
		self, 
		ctx: commands.Context, 
		image: discord.Attachment,
		transparent: str="True",
		direction: str = "left",
		position: str = "up",
		transparent2: str = None,
		direction2: str = None,
	):
		if not image.content_type or "image" not in image.content_type:
			raise Exception("Not image")
		await ctx.defer()
		extension = image.filename.split(".")[-1]

		transparent = True if closest_match(transparent, transparent_aliases) == "True" else False
		direction = closest_match(direction, direction_aliases)
		position = closest_match(position, position_aliases)
		if transparent2 != None or direction2 != None:
			try:
				transparent2 = True if closest_match(transparent2, transparent_aliases) == "True" else False
			except:
				transparent2 = True
			try:
				direction2 = closest_match(direction2, direction_aliases)
			except:
				direction2 = "right" if direction == "left" else "left"

		speechbubbled = edit_image(
			Image.open(BytesIO(await image.read())),
			extension,
			speechbubble,
			transparent1=transparent,
			direction1=direction,
			position1=position,
			transparent2=transparent2,
			direction2=direction2
		)
		speechbubbled_discorded = discord.File(speechbubbled, filename=image.filename)
		await ctx.reply(
			file=speechbubbled_discorded,
			view=GifizeView() if extension != "gif" else MISSING,
			allowed_mentions=no_ping
		)
	
	@speechbubble.autocomplete(name="transparent")
	async def transparent_autocomplete(self, ctx, curr):
		return transparents
	
	@speechbubble.autocomplete(name="direction")
	async def direction_autocomplete(self, ctx, curr):
		return directions
	
	@speechbubble.autocomplete(name="position")
	async def position_autocomplete(self, ctx, curr):
		return positions
	
	@speechbubble.autocomplete(name="transparent2")
	async def transparent2_autocomplete(self, ctx, curr):
		return transparents
	
	@speechbubble.autocomplete(name="direction2")
	async def direction2_autocomplete(self, ctx, curr):
		return directions

	@speechbubble.error
	async def speechbubble_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])


def speechbubble(
	image: Image.Image,
	transparent1: bool,
	direction1: str,
	position1: str,
	transparent2: bool,
	direction2: str
	):

	image = image.convert(mode="RGBA")
	bubbles = [(direction1, transparent1, position1)]
	if direction2 != None:
		bubbles.append((direction2, transparent2, "down" if position1 == "up" else "up"))

	for direction, transparent, position in bubbles:
		bubble = Image.open(f"assets/memes/speechbubble_{direction}.png").convert("RGBA").resize(image.size)
		if position == "down":
			bubble = bubble.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

		if transparent:
			bubble_arr = np.array(bubble).astype(int)
			image_arr = np.array(image).astype(int)
			diff = image_arr - bubble_arr
			diff[diff < 0] = 0
			diff = diff.astype(np.uint8)
			image = Image.fromarray(diff, mode="RGBA")

		else:
			image.paste(bubble, (0,0), bubble)

	return image
