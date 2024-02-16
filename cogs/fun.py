import discord
from discord.ext import commands
from discord import app_commands
from random import randint, choice
import re

from utils.emojis import Emojis
from utils.shortcuts import no_ping, no_color

normal2sga_table = {
	"a": "ᔑ",
	"b": "ʖ",
	"c": "ᓵ",
	"d": "↸",
	"e": "ᒷ",
	"f": "⎓",
	"g": "⊣",
	"h": "⍑",
	"i": "╎",
	"j": "⋮",
	"k": "ꖌ",
	"l": "ꖎ",
	"m": "ᒲ",
	"n": "リ",
	"o": "𝙹",
	"p": "!¡",
	"q": "ᑑ",
	"r": "∷",
	"s": "ᓭ",
	"t": "ℸ",
	"u": "̣",
	"v": "⚍",
	"w": "∴",
	"x": "̇̇/",
	"y": "||",
	"z": "⨅"
}
sga2normal_table = {
	"ᔑ": "a",
	"ʖ": "b",
	"ᓵ": "c",
	"↸": "d",
	"ᒷ": "e",
	"⎓": "f",
	"⊣": "g",
	"⍑": "h",
	"╎": "i",
	"⋮": "j",
	"ꖌ": "k",
	"ꖎ": "l",
	"ᒲ": "m",
	"リ": "n",
	"𝙹": "o",
	"!¡": "p",
	"ᑑ": "q",
	"∷": "r",
	"ᓭ": "s",
	"ℸ": "t",
	"̣": "u",
	"⚍": "v",
	"∴": "w",
	"̇̇/": "x",
	"||": "y",
	"⨅": "z",
	"\u200b": ""
}

class FunCommands(commands.Cog, name="Развлечения"):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.hybrid_command(aliases=["ench", "зачаровать", "зачарить", "зачарь", "зачаруй", "утср", "утсрфте"],
				  description="Переводит сообщение на язык стола зачарования")
	@app_commands.describe(text="Текст, который нужно перевести на язык стола зачарований")
	async def enchant(self, ctx, *, text: str):
		enchanted = text
		for char in normal2sga_table:
			enchanted = enchanted.replace(char, normal2sga_table[char]+"\u200b")
		await ctx.reply(enchanted, allowed_mentions=no_ping)
	@enchant.error
	async def enchant_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply("Введите текст который хотите зачаровать")
		
	@commands.hybrid_command(aliases=["unench", "раззачаровать", "разчарить", "разчарь", "разчаруй", "гтутср", "гтутсрфте"],
				  description="Переводит сообщение с языка стола зачарования")
	@app_commands.describe(text="Текст, который нужно перевести с языка стола зачарований")
	async def unenchant(self, ctx, *, text: str):
		unenchanted = text
		for char in sga2normal_table:
			unenchanted = unenchanted.replace(char, sga2normal_table[char])
		await ctx.reply(unenchanted, allowed_mentions=no_ping)
	@unenchant.error
	async def unenchant_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply("Введите текст который хотите раззачаровать")

	@commands.hybrid_command(aliases=["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
				  description="Генерирует рандомное число в заданном промежутке")
	@app_commands.describe(minimum="Минимальное число в промежутке", maximum="Максимальное число в промежутке")
	async def randomrange(self, ctx, minimum: str='-2147483648', maximum: str='2147483647'):
		minInt, maxInt = -2147483648, 2147483647
		clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
		minimum, maximum = clamp(int(float(minimum)), minInt, maxInt), clamp(int(float(maximum)), minInt, maxInt)
		minimum = min(minimum, maximum)
		maximum = max(minimum, maximum)
		result = randint(minimum, maximum)
		embed = discord.Embed(color=no_color, title=f"Рандомное число между {minimum} и {maximum}:")
		embed.add_field(name=result, value='', inline=True)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@randomrange.error
	async def randomrange_error(self, ctx, error):
		eArg = str(error).split("'")[1].replace("\\\\", "\\")
		await ctx.reply(f"❗ Неверно введённый аргумент - `{eArg}`. Допускаются только целочисленные значения", allowed_mentions=no_ping)

	@commands.hybrid_command(aliases=["rand", "r", "rng", "рандом", "ранд", "случайный-ответ", "сгенерь-ответ", "кфтвщь", "кфтв", "к", "ктп"],
				  description="Выдаёт случайный ответ из заданных на вопрос. [text] разделяется символом \"|\" или переносом строки")
	@app_commands.describe(text="Текст вопроса и ответов. Разделяются символом \"|\" или переносом строки")
	async def random(self, ctx, *, text: str):
		pattern = r'[|\n]'
		args = re.split(pattern, text)[1:]
		title = re.split(pattern, text)[0]
		result = choice(args)
		embed = discord.Embed(title=title, color=no_color)
		embed.add_field(name="Ответ:", value=result, inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@random.error
	async def random_error(self, ctx, error):
		embed = discord.Embed(title="Не хватает аргументов?", color=no_color)
		embed.add_field(name="Ответ:", value="Да")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	
	@commands.hybrid_command(name="look-for", aliases=["q"])
	async def look_for(self, ctx, game: str, *, details: str):
		# Building embed
		embed = discord.Embed(title=f"🔎 Ищу тиммейта для {game}", color=no_color)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
		embed.add_field(name="Подробности", value=details, inline=False)
		embed.add_field(name="✅Присоединились", value="")
		embed.add_field(name="❎Отклонили", value="")
		if game in ["minecraft", "terraria", "gartic"]:
			game_banner = discord.File(f"assets/game_banners/{game}.png", filename="say_gex.png")
			embed.set_image(url="attachment://say_gex.png")
		await ctx.send(embed=embed, view=LookFor(), file=game_banner)


class LookFor(discord.ui.View):
	def __init__(self):
		super().__init__()
	
	async def response(ctx, action):
		# Setting up variables
		embed = ctx.message.embeds[0]
		joined_users = embed.fields[1].value.split("\n")
		declined_users = embed.fields[2].value.split("\n")
		action_users_list = joined_users if action == "join" else declined_users
		opposite_users_list = declined_users if action == "join" else joined_users
		# Building embed
		usr_ping = ctx.user.mention
		if usr_ping not in action_users_list:
			action_users_list.append(usr_ping)
		else:
			action_users_list.remove(usr_ping)
		if usr_ping in opposite_users_list:
			opposite_users_list.remove(usr_ping)
		embed.set_field_at(1, name=embed.fields[1].name, value="\n".join(joined_users))
		embed.set_field_at(2, name=embed.fields[2].name, value="\n".join(declined_users))
		await ctx.response.edit_message(embed=embed, attachments=[])
	
	@discord.ui.button(label="Присоединится", emoji=Emojis.android, style=discord.ButtonStyle.gray)
	async def join(self, ctx: discord.Interaction, button: discord.ui.Button):
		await LookFor.response(ctx, "join")
	
	@discord.ui.button(label="Отказатся", emoji=Emojis.exe, style=discord.ButtonStyle.gray)
	async def decline(self, ctx: discord.Interaction, button: discord.ui.Button):
		await LookFor.response(ctx, "decline")
