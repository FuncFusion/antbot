import discord
from discord.ext import commands
from discord import app_commands

from random import choice, randint
import re

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


class RandomCommands(commands.Cog):

	@commands.hybrid_command(
		aliases=["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
		description="Генерирует рандомное число в заданном промежутке.",
		usage="`/randomrange <минимальное число в диапазоне> <максимальное число в диапазоне>`",
		help="### Пример:\n`/randomrange -69 420`")
	@app_commands.describe(minimum="Минимальное число в промежутке", maximum="Максимальное число в промежутке")

	async def randomrange(self, ctx, minimum: str='-2147483648', maximum: str='2147483647'):
		minInt, maxInt = -2147483648, 2147483647
		clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
		minimum, maximum = clamp(int(float(minimum)), minInt, maxInt), clamp(int(float(maximum)), minInt, maxInt)
		if minimum > maximum:
			minimum, maximum = maximum, minimum
		result = randint(minimum, maximum)
		embed = discord.Embed(color=no_color)
		embed.description = f"# {Emojis.dice} Рандомное число между {minimum} и {maximum}:\n## {result}"
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@randomrange.error
	async def randomrange_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "ValueError",
				"msg": "Допускаются только целочисленные занчения, между числами должен быть пробел"
			}
		])


	@commands.hybrid_command(
		aliases=["rand", "r", "rng", "рандом", "ранд", "случайный-ответ", "сгенерь-ответ", "кфтвщь", "кфтв", "к", "ктп"],
		description="Выдаёт случайный ответ на вопрос одним из заданных ответов.",
		usage="`/random <вопрос>|<ответ1>|<ответ2>`\n\n`!random <вопрос>\n<ответ1>\n<ответ2>`",
		help="Вопрос и ответы можно разделять символом \"|\" или переносом строки.\n### Пример:\n`/random Когда мне делать мой датапак?|Сегодня|Завтра|Никогда, забей на него`")
	@app_commands.describe(text="Текст вопроса и ответов. Разделяются символом \"|\" или переносом строки")

	async def random(self, ctx, *, text: str):
		pattern = r'[|\n]'
		args = re.split(pattern, text)[1:]
		title = re.split(pattern, text)[0]
		result = choice(args)
		embed = discord.Embed(color=no_color)
		embed.description = f"# {title}\n## {Emojis.dice} Ответ:\n{result}"
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@random.error
	async def random_error(self, ctx, error):
		embed = discord.Embed(title=f"{Emojis.exclamation_mark} Не хватает аргументов?", color=no_color)
		embed.description = f"# {Emojis.exclamation_mark} Не хватает аргументов?\n## {Emojis.dice} Ответ:\nДа"
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
