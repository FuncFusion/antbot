import discord
from discord.ext import commands
from discord import app_commands

from random import choice, randint
import re

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


class RandomCommands(commands.Cog):

	@commands.hybrid_command(aliases=["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
		description="Генерирует рандомное число в заданном промежутке")
	@app_commands.describe(minimum="Минимальное число в промежутке", maximum="Максимальное число в промежутке")

	async def randomrange(self, ctx, minimum: str='-2147483648', maximum: str='2147483647'):
		minInt, maxInt = -2147483648, 2147483647
		clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
		minimum, maximum = clamp(int(float(minimum)), minInt, maxInt), clamp(int(float(maximum)), minInt, maxInt)
		if minimum > maximum:
			minimum, maximum = maximum, minimum
		result = randint(minimum, maximum)
		embed = discord.Embed(color=no_color, title=f"Рандомное число между {minimum} и {maximum}:")
		embed.add_field(name=result, value='', inline=True)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@randomrange.error
	async def randomrange_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "ValueError",
				"msg": "Допускаются только целочисленные занчения"
			}
		])


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
		embed = discord.Embed(title=f"{Emojis.exclamation_mark} Не хватает аргументов?", color=no_color)
		embed.add_field(name="Ответ:", value="Да")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
