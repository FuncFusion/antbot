import discord
from discord.ext import commands
from discord import app_commands
from asyncio import sleep
from datetime import timedelta
from re import findall
from Levenshtein import distance

from utils.msg_utils import Emojis

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

help_attrs = {'name': 'help', 'aliases': ["helps", "хелп", "h", "рудз", "рудзы", "х", "р"]}
class CustomHelpCommand(commands.HelpCommand):

	async def send_bot_help(self, mapping):
		embed = discord.Embed(title="Список команд AntBot-a", color=no_color)
		thumbnail = discord.File("assets/pfps/online.png", filename="online.png")
		embed.set_thumbnail(url="attachment://online.png")
		for cog, cmds in mapping.items():
			cmd_str = ", ".join(f"`{cmd.name}`" for cmd in cmds)
			cmd_signature = [self.get_command_signature(cmd) for cmd in cmds]
			cog_name = getattr(cog, "qualified_name", "no_help")
			if not cog_name.startswith("no_help"):
				embed.add_field(name=cog_name, value=cmd_str, inline=False)
		await self.context.reply(embed=embed, file=thumbnail, allowed_mentions=no_ping)
	
	async def send_command_help(self, cmd):
		embed = discord.Embed(title=f"Команда `{cmd.name}`", color=no_color)
		embed.description = cmd.description
		params = ""
		if cmd.clean_params != {}: params = " " + " ".join(f"[{param}]" for param in cmd.clean_params)
		embed.add_field(name="Использование", value=f"`{self.context.clean_prefix}{cmd.name}{params}`", inline=False)
		alias_str = ", ".join(f"`{alias}`" for alias in cmd.aliases)
		embed.add_field(name="Алиасы", value=alias_str, inline=False)
		await self.context.reply(embed=embed, allowed_mentions=no_ping)
	
	async def command_not_found(self, string: str) -> str:
		possible_cmds, assumption = [], ""
		for cmd in self.context.bot.commands:
			if distance(string, cmd.name) <= len(cmd.name)/2:
				possible_cmds.append(cmd.name)
		if possible_cmds != []:
			cmds_str = "\n".join(f"`{cmd}`" for cmd in possible_cmds)
			assumption = f" Возможно, вы имели ввиду:\n{cmds_str}"
		await self.context.reply(f"Не нашёл такой команды - `{string.replace('`', ' ')}`.{assumption}", allowed_mentions=no_ping)

	async def subcommand_not_found(self, cmd, string) -> str:
		await CustomHelpCommand.send_command_help(self, cmd)

	async def send_cog_help(self, cog):
		await CustomHelpCommand.command_not_found(self, cog.qualified_name)


class GeneralCommands(commands.Cog, name="Общие"):
	def __init__(self, bot):
		self._original_help_command = bot.help_command
		bot.help_command = CustomHelpCommand(command_attrs=help_attrs)
		bot.help_command.cog = self
		self.bot = bot

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

	@commands.hybrid_command(name="server-info", aliases=["info", "server", "si", "сервер-инфо", "инфо", "сервер", "си", "ыукмукштащ", "штащ", "ыукмук", "ыш"],
		description="Показывает информацию о сервере")
	async def serverinfo(self, ctx):
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
		embed = discord.Embed(title=server.name, color=server.owner.color)
		embed.set_thumbnail(url=server.icon.url)
		embed.add_field(name="Владелец", value=f"{Emojis.crown} <@{server.owner_id}>", inline=False)
		embed.add_field(name="Сервер создан", value=f"{Emojis.calendar} <t:{int(server.created_at.timestamp())}>", inline=False)
		embed.add_field(name="Участники", value=f"{Emojis.users} {member_count} • {Emojis.bot} {bot_count}", inline=False)
		embed.add_field(name="Каналы", value=f"{Emojis.text_channel} {len(server.text_channels)} • {Emojis.speaker} {len(server.voice_channels)} • {Emojis.chat_type} {len(server.forums)}", inline=False)
		embed.add_field(name="Роли", value=f"{Emojis.role} {len(server.roles)}", inline=False)
		embed.add_field(name="Приглашение (иссякает через сутки)", value=f"{Emojis.link} {invitation_link}")
		embed.set_footer(text=f"🆔 {server.id}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
		
	@commands.hybrid_command(aliases=["usr", "u", "юзер", "пользователь", "усер", "гыук", "гык", "г"],
		description="Показывает информацию о пользователе")
	@app_commands.describe(user="Пользователь, информацию о котором вы хотите узнать")
	async def user(self, ctx, user:discord.Member=None):
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
		embed = discord.Embed(title=user.display_name, color=user.color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Присоединился к серверу", value=f"{Emojis.calendar} <t:{int(user.joined_at.timestamp())}>", inline=False)
		embed.add_field(name="Зарегистрировался(ась)", value=f"{Emojis.calendar} <t:{int(user.created_at.timestamp())}>", inline=False)
		embed.add_field(name="Роли", value=" ".join([role.mention for role in user.roles[1:][::-1]]), inline=False)
		embed.add_field(name="Статус", value=statuses[str(user.status)], inline=False)
		embed.set_footer(text=f"🆔 {user.id}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	
	@commands.hybrid_command(aliases=["s", "сказать", "молвить", "сей", "сэй", "ыфн", "ы"],
		description="Отправляет сообщение от имени бота")
	@app_commands.describe(text="Текст сообщения, которое отправит бот")
	@app_commands.default_permissions(manage_messages=True)
	async def say(self, ctx, *, text: str):
		temp = await ctx.send("_ _", ephemeral=True)
		await ctx.channel.send(text)
		await temp.delete()
		await ctx.message.delete()
	@say.error
	async def say_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply(f"{Emojis.exclamation_mark} Введите текст который хотите сказать от моего имени")

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
		error_msg = str(error)
		missing_args = {
			"time": f"{Emojis.exclamation_mark} Укажите через какое время хотите установить напоминание в формате <время><мера измерения времени сокращённо>",
			"reason": f"{Emojis.exclamation_mark} Укажите напоминание"
		}
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply(missing_args[error_msg.split(" ")[0]], allowed_mentions=no_ping, delete_after=4)
		elif "IndexError" in error_msg:
			await ctx.reply(missing_args["time"], allowed_mentions=no_ping, delete_after=4)
