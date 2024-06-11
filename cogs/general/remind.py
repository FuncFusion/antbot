import discord
from discord.ext import commands
from discord import app_commands

from asyncio import sleep
from re import findall

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping

time_multipliers = {
	"y": 31556952,
	"mo": 2678400,
	"w": 604800,
	"d": 86400,
	"h": 3600,
	"m": 60,
	"s": 1,
	"г": 31556952,
	"ме": 2678400,
	"н": 604800,
	"д": 86400,
	"ч": 3600,
	"м": 60,
	"с": 1
}
time_names = {
	"секунд": ["s", "с"],
	"минут": ["m", "м"],
	"часов": ["h", "ч"],
	"дней": ["d", "д"],
	"недель": ["w", "н"],
	"месяцев": ["mo", "ме"],
	"лет": ["y", "г"]
}


class RemindCommand(commands.Cog):
	@commands.hybrid_command(aliases=["reminder", "rem", "alarm", "remind-me", "remindme", "напомнить", "напоминатель", "напомни", "будильник", "нап", "куьштв", "куьштвук", "куь", "фдфкь", "куьштв-ьу", "куьштвьу"],
		description="Напоминает о чём-то через определённое время с помощью пинга.")
	@app_commands.describe(time="Время, через которое бот пинганёт", reason="Причина, по которой бот будет напоиминать")
	async def remind(self, ctx, time:str, *, reason:str):
		raw_time = findall(r"[0-9]+", time)
		measure = findall(r"[A-zА-я]+", time)
		time = int(raw_time[0]) * time_multipliers[measure[0]]
		time_name = ""
		for key, values in time_names.items():
			if measure[0] in values: time_name = key
		user = ctx.author
		embed = discord.Embed(title="🔔 Напоминание", color=no_color)
		embed_reason = ""
		if reason != "":
			embed_reason = f"по причине \"{reason}\""
		if time < 1262278080:
			if reason != "": embed.add_field(name=reason, value="", inline=False)
			await ctx.reply(f"Я вас упомяну через {raw_time[0]} {time_name} {embed_reason}", allowed_mentions=no_ping)
			await sleep(time)
			await ctx.send(user.mention,embed=embed)
		else:
			await ctx.reply(f"{Emojis.exclamation_mark} Вы указали слишком большой промежуток времени.", allowed_mentions=no_ping)
	@remind.error
	async def remind_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"contains": "time",
				"msg": f"{Emojis.exclamation_mark} Укажите через какое время хотите установить напоминание в формате <время><мера измерения времени сокращённо>"
			},
			{
				"exception": commands.MissingRequiredArgument,
				"contains": "reason",
				"msg": f"{Emojis.exclamation_mark} Укажите напоминание"
			},
			{
				"contains": "IndexError",
				"msg": f"{Emojis.exclamation_mark} Укажите через какое время хотите установить напоминание в формате <время><мера измерения времени сокращённо>"
			}
		])
	