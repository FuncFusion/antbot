import discord
from discord.ext import commands

from PIL import Image
import numpy as np
from io import BytesIO

from utils import handle_errors, edit_image


sb_original = Image.open("assets/memes/speechbubble.png").convert("RGBA")


class SpeechbubbleCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["ызуусригииду", "спичбабл", "спичбаббл", "сб", "sb"],
		description="Вставляет на изображение удивленных сойджаков",
		usage="`/speechbubble <изображение>`",
		help="### Пример:\n`/speechbubble image.png`"
	)

	async def speechbubble(self, ctx: commands.Context, image: discord.Attachment):
		if "image" not in image.content_type:
			raise Exception("Not image")
		speechbubbled = edit_image(
			Image.open(BytesIO(await image.read())),
			image.filename.split(".")[-1],
			speechbubble
		)
		speechbubbled_discorded = discord.File(speechbubbled, filename=image.filename)
		await ctx.send(file=speechbubbled_discorded)

	@speechbubble.error
	async def speechbubble_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not image",
				"msg": "Это не изображение"
			}
		])


def speechbubble(image: Image.Image):
	sb_image = sb_original.copy()
	sb_image = sb_image.resize((image.width, image.height))
	
	sb_arr = np.array(sb_image).astype(int)
	image_arr = np.array(image.convert(mode="RGBA")).astype(int)

	diff = image_arr - sb_arr
	diff[diff < 0] = 0
	diff = diff.astype(np.uint8)

	return Image.fromarray(diff, mode="RGBA")
