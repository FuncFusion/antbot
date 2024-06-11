import discord
from discord.ext import commands

from PIL import Image, ImageDraw, ImageFont
from random import choice
import io

from settings import LEAVES_CHANNEL_ID, JOINS_CHANNEL_ID


async def generate_banner(user):
	def fit_size(base, limit, font_path, text):
		font_size = base
		font = ImageFont.truetype(font_path, base)
		while \
		(hitbox:=banner_draw.textbbox((0,0), text, font=font))[2] - hitbox[0] >= limit:
			font_size -= 2
			font = ImageFont.truetype(font_path, font_size)
		return font
	# Pasting avatar
	greeting_banner = Image.open("assets/greeting_banner.png")
	avatar = await user.avatar.read()
	avatar = Image.open(io.BytesIO(avatar)).resize((312, 312))
	avatar = avatar.crop((0, 0, 312, 289))
	greeting_banner.paste(avatar,  (190, 54), avatar)
	# Name
	banner_draw = ImageDraw.Draw(greeting_banner)
	m10_font = fit_size(100, 768, "assets/fonts/m10.ttf", user.display_name)
	m5_font = fit_size(40, 512, "assets/fonts/m5.otf", user.name)
	banner_draw.text((921, 240), user.display_name, font=m10_font, fill="white", anchor="mm")
	banner_draw.text((921, 340), user.name, font=m5_font, fill="white", anchor="mm")
	#
	file_greeting = io.BytesIO()
	greeting_banner.save(file_greeting, format="PNG")
	file_greeting.seek(0)
	greeting_image = discord.File(file_greeting, filename="saygex.png")
	return greeting_image


class JoinAndLeaveMessage(commands.Cog):
	def __init__(self, bot):
		self.LEAVES_CHANNEL = bot.get_channel(LEAVES_CHANNEL_ID)
		self.JOINS_CHANNEL = bot.get_channel(JOINS_CHANNEL_ID)

	@commands.Cog.listener
	async def on_member_join(self, user):
		greeting_msg = choice([
			"Добро пожаловать, {0}. Мы надеемся что ты принёс пиццу",
			"Добро пожаловать, {0}",
			"{0} тут",
			"Поприветствуйте {0}",
			"Ради тебя видеть, {0}",
			"{0} только что приземлился",
			"Дикий {0} присоединился"
		])
		greeting_image = await generate_banner(user)
		await self.JOINS_CHANNEL.send(greeting_msg.format(user.mention), file=greeting_image)
	
	@commands.Cog.listener
	async def on_member_remove(self, user):
		leaving_msg = choice([
			"{0} куда",
			"{0} ливнул"
		])
		leaving_image = await generate_banner(user)
		await self.LEAVES_CHANNEL.send(leaving_msg.format(user.mention), file=leaving_msg)