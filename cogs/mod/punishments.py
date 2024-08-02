import discord
from discord.ext import commands
from discord import app_commands

from re import findall
from random import choice
from typing import Union
from datetime import timedelta

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color
from utils.time import get_secs

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

def generate_stupid_reason():
    return choice([
        "Настолько жалок, что даже не достоин причины",
        "Ты хочешь показать всем свою неадекватность? Опозорится самому, опозорить честь сервера?",
        "Короче: читы - бан; кемперство - бан; оскорбление - бан; оскорбление администрации - расстрел, а потом бан",
		"https://tenor.com/view/lfmods-modsquad-bestmodsintheworld-nickfifs-thanos-gif-20839877"
    ])


class PunishmentCommands(commands.Cog, name="Модерация"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["ифт", "бан", "банчек", "заблокировать"])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.ban(reason=reason)
		#
		embed = discord.Embed(title=f"{Emojis.ban} Бан", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Забаненый участник", value=f"{user.name}({user.mention})", inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@ban.error
	async def ban_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите пользователя"
			},
			{
				"contains": "Forbidden",
				"msg": "Кудааа, не туда воюешь"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
	
	@commands.command(aliases=["гтиат", "анбан", "разблокировать"])
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, user: Union[discord.Member, discord.User]):
		await ctx.guild.unban(user)
		#
		embed = discord.Embed(title=f"{Emojis.ban} Разбан", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Разабаненый участник", value=f"{user.name}({user.mention})", inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@ban.error
	async def ban_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите пользователя"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
		
	@commands.command(aliases=["ьгеу", "мут"])
	@commands.has_permissions(moderate_members=True)
	async def mute(self, ctx, user: discord.Member, term: str, *, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.timeout(timedelta(seconds=get_secs(term)), reason=reason)
		#
		embed = discord.Embed(title=f"{Emojis.mute} Мут", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Замученый участник", value=user.mention, inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@mute.error
	async def mute_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "user",
				"msg": "Пожалуйста, укажите пользователя"
			},
			{
				"contains": "term",
				"msg": "Пожалуйста, укажите срок мута в формате <время><мера измерения времени сокращённо>"
			},
			{
				"exception": commands.MemberNotFound,
				"msg": "Пользователь не найден"
			},
			{
				"contains": "IndexError",
				"msg": "Пожалуйста, укажите срок мута в формате <время><мера измерения времени сокращённо>"
			},
			{
				"contains": "KeyError",
				"msg": "Неверная мера измерения времени"
			},
			{
				"contains": "Forbidden",
				"msg": "Кудааа, не туда воюешь"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
		
	@commands.command(aliases=["лшсл", "кик", "изгнать"])
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, *, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.kick(reason=reason)
		embed = discord.Embed(title=f"{Emojis.door}Кик", color=no_color)
		embed.set_thumbnail(url=user.avatar.url)
		embed.add_field(name="Вершитель судьбы", value=ctx.author.mention)
		embed.add_field(name="Причина", value=reason)
		embed.add_field(name="Кикнутый участник", value=f"{user.name}({user.mention})", inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@kick.error
	async def kick_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите пользователя"
			},
			{
				"exception": commands.MemberNotFound,
				"msg": "Пользователь не найден"
			},
			{
				"contains": "Forbidden",
				"msg": "Э, не туда воюешь"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
		