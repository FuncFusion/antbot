import discord
from discord.ext import commands
from discord import app_commands
from asyncio import sleep
from datetime import timedelta
from re import findall

from utils.shortcuts import no_ping, no_color

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

class GeneralCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(name="server-info", aliases=["info", "server", "si","сервер-инфо", "инфо", "сервер", "си", "ыукмукштащ", "штащ", "ыукмук", "ыш"],
							description="Показывает информацию о сервере")
		async def serverinfo(ctx):
			# setup vars
			server = ctx.guild
			member_count = 0
			bot_count = 0
			for member in server.members:
				if member.bot:
					bot_count += 1
				else:
					member_count += 1
			invitation_link = await ctx.channel.create_invite(max_age=86400)
			# Building embed
			embed = discord.Embed(title=server.name, color=server.owner.color)
			embed.set_thumbnail(url=server.icon.url)
			embed.add_field(name="Владелец", value=f"👑 <@{server.owner_id}>", inline=False)
			embed.add_field(name="Сервер создан", value=f"📅 <t:{int(server.created_at.timestamp())}>", inline=False)
			embed.add_field(name="Участники", value=f"👤 {member_count} • 🤖 {bot_count}", inline=False)
			embed.add_field(name="Каналы", value=f"⌨ {len(server.text_channels)} • 🔊 {len(server.voice_channels)} • 💬 {len(server.forums)}", inline=False)
			embed.add_field(name="Роли", value=f"🎭 {len(server.roles)}", inline=False)
			embed.add_field(name="Приглашение (иссякает через сутки)", value=f"🔗 {invitation_link}")
			embed.set_footer(text=f"🆔 {server.id}")
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		
		@bot.hybrid_command(aliases=["usr", "u", "юзер", "пользователь", "усер", "гыук", "гык", "г"],
					  description="Показывает информацию о пользователе")
		async def user(ctx, user:discord.Member=None):
			# Setting up vars
			if user == None:
				user = ctx.author
			statuses = {
				"online": "🟢 В сети",
				"offline": "⚫ Не в сети",
				"idle": "🟡 Отошёл",
				"dnd": "🔴 Не беспокоить",
				"invisible": "⚫ Невидимка"
			}
			# Build embed
			embed = discord.Embed(title=user.display_name, color=user.color)
			embed.set_thumbnail(url=user.avatar.url)
			embed.add_field(name="Присоединился к серверу", value=f"📅 <t:{int(user.joined_at.timestamp())}>", inline=False)
			embed.add_field(name="Зарегистрировался(ась)", value=f"📅 <t:{int(user.created_at.timestamp())}>", inline=False)
			embed.add_field(name="Роли", value=" ".join([role.mention for role in user.roles[1:][::-1]]), inline=False)
			embed.add_field(name="Статус", value=statuses[str(user.status)], inline=False)
			embed.set_footer(text=f"🆔 {user.id}")
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		
		@bot.hybrid_command(aliases=["s", "сказать", "молвить", "сей", "сэй", "ыфн", "ы"],
							description="Отправляет сообщение от имени бота")
		@app_commands.describe(text="Текст сообщения, которое отправит бот")
		@app_commands.default_permissions(manage_messages=True)
		async def say(ctx, *, text: str):
			temp = await ctx.send("_ _", ephemeral=True)
			await ctx.channel.send(text)
			await temp.delete()
			await ctx.message.delete()
		@say.error
		async def say_error(ctx, error):
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply("Введите текст который хотите сказать от моего имени")

		@bot.hybrid_command(aliases=["reminder", "rem", "alarm", "remind-me", "remindme", "напомнить", "напоминатель", "напомни", "будильник", "нап", "куьштв", "куьштвук", "куь", "фдфкь", "куьштв-ьу", "куьштвьу"],
					  description="Напоминает о чём-то через определённое время с помощью пинга.")
		@app_commands.describe(time="Время, через которое бот пинганёт", reason="Причина, по которой бот будет напоиминать")
		async def remind(ctx, time:str, *, reason:str):
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
				await ctx.reply("❗ Вы указали слишком большой промежуток времени.", allowed_mentions=no_ping)
		@remind.error
		async def remind_error(ctx, error):
			print(error , type(error))
			error_msg = str(error)
			missing_args = {
				"time": "Укажите через какое время хотите установить напоминание в формате <время><мера измерения времени сокращённо>",
				"reason": "Укажите напоминание"
			}
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply(missing_args[error_msg.split(" ")[0]], allowed_mentions=no_ping)
			elif "IndexError" in error_msg:
				await ctx.reply(missing_args["time"], allowed_mentions=no_ping)
