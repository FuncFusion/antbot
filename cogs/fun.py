import discord
from discord.ext import commands
from discord import app_commands
from random import randint, choice
import re

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
		
		@bot.hybrid_command(aliases=["ench", "зачаровать", "зачарить", "зачарь", "зачаруй", "утср", "утсрфте"],
					  description="Переводит сообщение на язык стола зачарования")
		@app_commands.describe(text="Текст, который нужно перевести на язык стола зачарований")
		async def enchant(ctx, *, text: str):
			enchanted = text
			for char in normal2sga_table:
				enchanted = enchanted.replace(char, normal2sga_table[char]+"\u200b")
			await ctx.reply(enchanted, allowed_mentions=no_ping)
		@enchant.error
		async def enchant_error(ctx, error):
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply("Введите текст который хотите зачаровать")
		
		@bot.hybrid_command(aliases=["unench", "раззачаровать", "разчарить", "разчарь", "разчаруй", "гтутср", "гтутсрфте"],
					  description="Переводит сообщение с языка стола зачарования")
		@app_commands.describe(text="Текст, который нужно перевести с языка стола зачарований")
		async def unenchant(ctx, *, text: str):
			unenchanted = text
			for char in sga2normal_table:
				unenchanted = unenchanted.replace(char, sga2normal_table[char])
			await ctx.reply(unenchanted, allowed_mentions=no_ping)
		@unenchant.error
		async def unenchant_error(ctx, error):
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply("Введите текст который хотите раззачаровать")

		@bot.hybrid_command(aliases=["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
					  description="Генерирует рандомное число в заданном промежутке")
		@app_commands.describe(first="Минимальное число в промежутке", second="Максимальное число в промежутке")
		async def randomrange(ctx, first: str='-2147483648', second: str='2147483647'):
			minInt, maxInt = -2147483648, 2147483647
			clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
			first, second = clamp(int(float(first)), minInt, maxInt), clamp(int(float(second)), minInt, maxInt)
			minimum = min(first, second)
			maximum = max(first, second)
			result = randint(minimum, maximum)
			embed = discord.Embed(color=no_color, title=f"Рандомное число между {minimum} и {maximum}:")
			embed.add_field(name=result, value='', inline=True)
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		@randomrange.error
		async def randomrange_error(ctx, error):
			eArg = str(error).split("'")[1].replace("\\\\", "\\")
			await ctx.reply(f"❗ Неверно введённый аргумент - `{eArg}`. Допускаются только целочисленные значения", allowed_mentions=no_ping)

		@bot.hybrid_command(aliases=["rand", "r", "rng", "рандом", "ранд", "случайный-ответ", "сгенерь-ответ", "кфтвщь", "кфтв", "к", "ктп"],
					  description="Выдаёт случайный ответ из заданных на заданный вопрос")
		@app_commands.describe(text="Текст вопроса и ответов. Разделяются символом \"|\" или переносом строки")
		async def random(ctx, *, text: str):
			pattern = r'[|\n]'
			args = re.split(pattern, text)[1:]
			title = re.split(pattern, text)[0]
			result = choice(args)
			embed = discord.Embed(title=title, color=no_color)
			embed.add_field(name="Ответ:", value=result, inline=False)
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		@random.error
		async def random_error(ctx, error):
			embed = discord.Embed(title="Не хватает аргументов?", color=no_color)
			embed.add_field(name="Ответ:", value="Да")
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
