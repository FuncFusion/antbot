import discord
from discord.ext import commands
from discord import app_commands

from re import findall
from random import choice
from asyncio import sleep
from datetime import timedelta

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

class ModerationCommands(commands.Cog):
	def generate_stupid_reason():
		return choice([
			"Настолько жалок, что даже не достоин причины",
			"Ты хочешь показать всем свою неадекватность? Опозорится самому, опозорить честь сервера?",
			"Ой, кажется не та команда..",
			"Смари как могу",
			"Хоть я и не атлет, но и не скибиди туалет",
			"Короче: читы - бан; кемперство - бан; оскорбление - бан; оскорбление администрации - расстрел, а потом бан"
		])
	
	def __init__(self, bot):
		
		@bot.command(aliases=["ифт", "бан", "банчек", "заблокировать"])
		@app_commands.default_permissions(ban_members=True)
		async def ban(ctx, user: discord.Member=None, term: str="", *, reason: str=None):
			# Setting up variables
			reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
			raw_term = findall(r"[0-9]+", term)
			measure = findall(r"[a-zA-Zа-яА-Я]+", term)
			# Handling errors
			if user == None:
				await ctx.send("Пожалуйста, укажите пользователя")
				return None
			elif term == "":
				await ctx.send("Пожалуйста, укажите срок бана в формате <время><мера измерения времени сокращённо>")
				return None
			elif raw_term == []:
				await ctx.send("Пожалуйста, укажите целочисленное время бана")
				return None
			elif measure == []:
				await ctx.send("Пожалуйтса, укажите меру измерения времени бана")
				return None
			term = int(raw_term[0]) * time_multipliers[measure[0]]
			# Building embed
			embed = discord.Embed(title="🔨Бан", color=discord.Color.dark_embed())
			embed.set_thumbnail(url=user.avatar.url)
			embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
			embed.add_field(name="Причина", value=reason)
			embed.add_field(name="Забаненый участник", value=f"{user.name}({user.mention})", inline=False)
			await ctx.send(embed=embed)
			# Ban
			await user.ban(reason=reason)
			# Unban
			if term < 1262278080:
				await sleep(term)
				await user.unban()
		
		@bot.command(aliases=["ьгеу", "мут"])
		@app_commands.default_permissions(mute_members=True)
		async def mute(ctx, user: discord.Member=None, term: str="", *, reason: str=None):
			# Setting up variables
			reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
			raw_term = findall(r"[0-9]+", term)
			measure = findall(r"[a-zA-Zа-яА-Я]+", term)
			# Handling errors
			if user == None:
				await ctx.send("Пожалуйста, укажите пользователя")
				return None
			elif term == "":
				await ctx.send("Пожалуйста, укажите срок мута в формате <время><мера измерения времени сокращённо>")
				return None
			elif raw_term == []:
				await ctx.send("Пожалуйста, укажите целочисленное время мута")
				return None
			elif measure == []:
				await ctx.send("Пожалуйтса, укажите меру измерения времени мута")
				return None
			term = int(raw_term[0]) * time_multipliers[measure[0]]
			# Building embed
			embed = discord.Embed(title="🔇Мут", color=discord.Color.dark_embed())
			embed.set_thumbnail(url=user.avatar.url)
			embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
			embed.add_field(name="Причина", value=reason)
			embed.add_field(name="Замуненый участник", value=user.mention, inline=False)
			await ctx.send(embed=embed)
			# Da mute
			await user.timeout(timedelta(seconds=term), reason=reason)
		
		@bot.command(aliases=["лшсл", "кик", "изгнать"])
		@app_commands.default_permissions(kick_members=True)
		async def kick(ctx, user: discord.Member=None, *, reason: str=None):
			# Setting up variables
			reason = reason if reason != None else ModerationCommands.generate_stupid_reason()
			# Handling errors
			if user == None:
				await ctx.send("Пожалуйста, укажите пользователя")
				return None
			# Building embed
			embed = discord.Embed(title="🦵Кик", color=discord.Color.dark_embed())
			embed.set_thumbnail(url=user.avatar.url)
			embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
			embed.add_field(name="Причина", value=reason)
			embed.add_field(name="Кикнутый участник", value=f"{user.name}({user.mention})", inline=False)
			await ctx.send(embed=embed)
			# Da kick
			await user.kick(reason=reason)