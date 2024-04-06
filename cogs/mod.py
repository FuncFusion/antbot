import discord
from discord.ext import commands
from discord import app_commands

from re import findall
from random import choice
from asyncio import sleep
from datetime import timedelta
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

class ModerationCommands(commands.Cog, name="Модерация"):
	def generate_stupid_reason():
		return choice([
			"Настолько жалок, что даже не достоин причины",
			"Ты хочешь показать всем свою неадекватность? Опозорится самому, опозорить честь сервера?",
			"Ой, кажется не та команда..",
			"Смари как могу",
			"Хоть я и не атлет, но и не скибиди туалет",
			"Короче: читы - бан; кемперство - бан; оскорбление - бан; оскорбление администрации - расстрел, а потом бан",
			"Не важно в какой жопе ты находишся. Важно, что бы в твоей жопе никто не находился"
		])
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases=["ифт", "бан", "банчек", "заблокировать"])
	@app_commands.default_permissions(ban_members=True)
	@app_commands.describe(user="Пользователь", reason="Причина бана")
	async def ban(self, ctx, user: discord.Member, reason: str=None):
		# Setting up variables
		reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
		# Ban
		await user.ban(reason=reason)
		# Building embed
		embed = discord.Embed(title="🔨Бан", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Забаненый участник", value=f"{user.name}({user.mention})", inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@ban.error
	async def ban_error(self, ctx, error):
		error_msg = str(error)
		if isinstance(error, commands.MissingRequiredArgument):
			if "user" in error_msg:
				await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите пользователя", allowed_mentions=no_ping)
		elif "Forbidden" in error_msg:
			await ctx.reply("Кудааа, не туда воюешь", allowed_mentions=no_ping)

		
	@commands.command(aliases=["ьгеу", "мут"])
	@app_commands.default_permissions(mute_members=True)
	@app_commands.describe(user="Пользователь", term="Срок мута", reason="Причина мута")
	async def mute(self, ctx, user: discord.Member, term: str, *, reason: str=None):
		# Setting up variables
		reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
		raw_term = findall(r"[0-9]+", term)
		measure = findall(r"[a-zA-Zа-яА-Я]+", term)
		term = int(raw_term[0]) * time_multipliers[measure[0]]
		# Da mute
		await user.timeout(timedelta(seconds=term), reason=reason)
		# Building embed
		embed = discord.Embed(title="🔇Мут", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Замученый участник", value=user.mention, inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@mute.error
	async def mute_error(self, ctx, error):
		error_msg = str(error)
		if isinstance(error, commands.MissingRequiredArgument):
			if "user" in error_msg:
				await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите пользователя", allowed_mentions=no_ping)
			elif "term" in error_msg:
				await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите срок мута в формате <время><мера измерения времени сокращённо>", allowed_mentions=no_ping)
		elif isinstance(error, commands.MemberNotFound):
			await ctx.reply(f"{Emojis.exclamation_mark} Пользователь `{error_msg.split('\"')[1]}` не найден", allowed_mentions=no_ping)
		elif "IndexError" in error_msg:
			await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите срок мута в формате <время><мера измерения времени сокращённо>", allowed_mentions=no_ping)
		elif "KeyError" in error_msg:
			await ctx.reply(f"{Emojis.exclamation_mark} `{error_msg.split('\'')[1]}` не является мерой измерения времени", allowed_mentions=no_ping)
		elif "Forbidden" in error_msg:
			await ctx.reply("Кудааа, не туда воюешь", allowed_mentions=no_ping)
		
	@commands.command(aliases=["лшсл", "кик", "изгнать"])
	@app_commands.default_permissions(kick_members=True)
	@app_commands.describe(user="Пользователь", reason="Причина кика")
	async def kick(self, ctx, user: discord.Member, *, reason: str=None):
		# Setting up variables
		reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
		# Da kick
		await user.kick(reason=reason)
		# Building embed
		embed = discord.Embed(title=f"{Emojis.door}Кик", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Кикнутый участник", value=f"{user.name}({user.mention})", inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@kick.error
	async def kick_error(self, ctx, error):
		error_msg = str(error)
		if isinstance(error, commands.MissingRequiredArgument):
			if "user" in error_msg:
				await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите пользователя", allowed_mentions=no_ping)
		elif isinstance(error, commands.MemberNotFound):
			await ctx.reply(f"{Emojis.exclamation_mark} Пользователь `{error_msg.split('\"')[1]}` не найден", allowed_mentions=no_ping)
		elif "Forbidden" in error_msg:
			await ctx.reply("Кудааа, не туда воюешь", allowed_mentions=no_ping)
		
	@commands.hybrid_command(aliases=["сдуфк", "клир", "очистить"], 
						description="Очищает сообщения")
	@app_commands.default_permissions(manage_messages=True)
	@app_commands.describe(count="Количество сообщений которое будет удалено", channel="Канал в котором будут удалены сообщения")
	async def clear(self, ctx, count: int=None, channel: discord.TextChannel=None):
		# Setting up variables
		channel = channel if channel != None else ctx.channel
		# Handling errors
		if count == None:
			await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите количество сообщений которое будет удалено", allowed_mentions=no_ping)
		else:
			# Building embed
			embed = discord.Embed(title="🗑 Очистка", color=no_color)
			embed.add_field(name="Канал", value=channel.jump_url, inline=False)
			embed.add_field(name="Удалённые сообщения", value=f"{Emojis.chat_type} {count}", inline=False)
			# Clearing
			await channel.purge(limit=count + (1 if channel == ctx.channel else 0))
			#
			await ctx.reply(embed=embed, allowed_mentions=no_ping)