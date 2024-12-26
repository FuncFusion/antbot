import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING

from PIL import Image, ImageDraw
from io import BytesIO
from re import search, compile

from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping
from utils.msg_utils import Emojis

color_regex = compile(
	r"(?P<hex>"
		r"(#(?P<hex_r>[a-fA-F\d]{2})(?P<hex_g>[a-fA-F\d]{2})(?P<hex_b>[a-fA-F\d]{2}))"
		r")|"
		r"(?P<rgb_float>"
		r"(?P<float_r>\d\.\d+)[\s\S]*?"
		r"(?P<float_g>\d\.\d+)[\s\S]*?"
		r"(?P<float_b>\d\.\d+)[\s\S]*?"
		r"(?P<float_a>\d\.\d+)?"
		r")|"
		r"(?P<rgb_int>"
		r"(?P<int_r>\d{1,3})[\s,][\s\S]*?"
		r"(?P<int_g>\d{1,3})[\s,][\s\S]*?"
		r"(?P<int_b>\d{1,3})[\s,]?[\s\S]*?"
		r"(?P<int_a>\d{1,3})?"
		r")|"
		r"(?P<decimal>"
		r"(?P<color>\d{1,9})"
		r")"
)

def to_rgb_int(color, type):
	match type:
		case "hex":
			return tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
		case "rgb_int":
			return tuple(map(int, color))
		case "rgb_float":
			return tuple(int(i * 255.0) for i in color)
		case "decimal":
			return (
				color // (256 ** 2),
				color // 256 % 256,
				color % 256,
				255
			)

def to_hex(color):
	r, g, b, _ = color
	return f"#{r:02x}{g:02x}{b:02x}".upper()

def to_rgb_float(color):
	return tuple(i / 255.0 for i in color)

def to_decimal(color):
	r, g, b, _ = color
	return r * 256 ** 2 + g * 256 + b

def generate_showcase(color):
	color = color[:-1]
	showcase_image = Image.open("assets/color/showcase.png").convert("RGBA")
	width, height = showcase_image.size
	pixels = showcase_image.load()
	# Multiply pixels with alpha 255 by a specific color
	for x in range(width):
		for y in range(height):
			r, g, b, a = pixels[x, y]
			if a == 255:
				pixels[x, y] = (r * color[0] // 255,
					g * color[1] // 255,
					b * color[2] // 255,
					a)
	draw = ImageDraw.Draw(showcase_image)
	square_position = (21, 2, 21 + 12, 2 + 12)
	draw.rectangle(square_position, fill=color)
	#
	showcase_bg = Image.open("assets/color/showcase_bg.png").convert("RGBA")
	showcase_bg.paste(showcase_image, (0, 0), showcase_image)
	new_size = (showcase_bg.width * 8, showcase_bg.height * 8)
	showcase_bg = showcase_bg.resize(new_size, Image.NEAREST)
	#
	showcase_fp = BytesIO()
	showcase_bg.save(showcase_fp, format="png")
	showcase_fp.seek(0)

	return showcase_fp


class ColorCommand(commands.Cog):
	
	@commands.hybrid_command(
		aliases=["c", "col", "сщдщк", "цвет", "ц", "с"],
		description="Конверирует цвет в hex, rgb float, rgb int, decimal и показывает его вид на кожанной броне и зелье",
		usage="`/color <цвет в формате hex|rgb float|rgb int|decimal>`", 
		help=""
	)
	async def color(self, ctx, *, color: str):
		color = search(color_regex, color)
		if color == None:
			raise Exception("Wrong type")
		if color.group("hex"):
			rgba_color = to_rgb_int(color.group("hex"), "hex")
		elif color.group("rgb_int"):
			rgba_color = list(int(color.group(f"int_{i}")) for i in "rgb")
			if (alpha:=color.group("int_a")):
				rgba_color.append(int(alpha))
			else:
				rgba_color.append(255)
			rgba_color = tuple(rgba_color)
		elif color.group("rgb_float"):
			rgba_float_color = list(float(color.group(f"float_{i}")) for i in "rgb")
			if (alpha:=color.group("float_a")):
				rgba_float_color.append(int(alpha))
			else:
				rgba_float_color.append(1.0)
			rgba_color = to_rgb_int(rgba_float_color, "rgb_float")
		elif color.group("decimal"):
			rgba_color = to_rgb_int(int(color.group("color")), "decimal")
		hex_color = to_hex(rgba_color)
		rgba_float_color = to_rgb_float(rgba_color)
		decimal_color = to_decimal(rgba_color)
		#
		embed = discord.Embed(
			color=no_color,
			description=f"## {Emojis.shader_triangle} Форматы цвета\n"
				f"**Hex** ```css\n{hex_color}```\n"
				f"**RGB float** ```c\n{str(rgba_float_color)[1:-1]}```\n"
				f"**RGB int** ```c\n{str(rgba_color)[1:-1]}```\n"
				f"**Decimal** ```c\n{decimal_color}```"
		)
		#
		showcase = generate_showcase(rgba_color)
		showcase_discord_file = discord.File(showcase, filename="showcase.png")
		embed.set_image(url="attachment://showcase.png")
		await ctx.reply(embed=embed, file=showcase_discord_file, allowed_mentions=no_ping)
	
	@color.error
	async def color_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не указан цвет"
			},
			{
				"contains": "Wrong type",
				"msg": "Неверный тип цвета"
			}
		])