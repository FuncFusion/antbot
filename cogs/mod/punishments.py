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


def generate_stupid_reason():
    return choice([
        "Настолько жалок, что даже не достоин причины",
        "Ты хочешь показать всем свою неадекватность? Опозорится самому, опозорить честь сервера?",
        "Короче: читы - бан; кемперство - бан; оскорбление - бан; оскорбление администрации - расстрел, а потом бан",
		"Ну всё, ты наказан 😈",
		"А нечего было всякую фигню творить",
		"Мдэ",
		"[Видеофиксация](https://www.youtube.com/watch?v=dQw4w9WgXcQ) его преступлений",
		"https://tenor.com/view/lfmods-modsquad-bestmodsintheworld-nickfifs-thanos-gif-20839877"
    ])


class PunishmentCommands(commands.Cog, name="Модерация"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["ифт", "бан", "банчек", "заблокировать"],
		description="**Модераторская команда.** Банит указанного пользователя.",
		usage="`/ban <пользователь> [причина]`",
		help="")
	@commands.has_permissions(ban_members=True)
	@app_commands.default_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.ban(reason=reason)
		#
		embed = discord.Embed(title=f"{Emojis.ban} Бан", color=no_color)
		embed.set_thumbnail(url=user.display_avatar.url)
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
				"msg": "Э, не туда воюешь"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
	
	@commands.hybrid_command(
		aliases=["гтиат", "анбан", "разблокировать"],
		description="**Модераторская команда.** Разбанивает указанного пользователя.",
		usage="`/unban <пользователь>`",
		help="")
	@commands.has_permissions(ban_members=True)
	@app_commands.default_permissions(ban_members=True)
	async def unban(self, ctx, user: Union[discord.Member, discord.User]):
		await ctx.guild.unban(user)
		#
		embed = discord.Embed(title=f"{Emojis.ban} Разбан", color=no_color)
		embed.set_thumbnail(url=user.display_avatar.url)
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
		
	@commands.hybrid_command(
		aliases=["ьгеу", "мут"],
		description="**Модераторская команда.** Мутит указанного пользователя.",
		usage="`/mute <пользователь> <время> [причина]`",
		help="")
	@commands.has_permissions(moderate_members=True)
	@app_commands.default_permissions(moderate_members=True)
	async def mute(self, ctx, user: discord.Member, term: str, *, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.timeout(timedelta(seconds=get_secs(term)), reason=reason)
		#
		embed = discord.Embed(title=f"{Emojis.mute} Мут", color=no_color)
		embed.set_thumbnail(url=user.display_avatar.url)
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
				"msg": "Э, не туда воюешь"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
		
	@commands.hybrid_command(
		aliases=["лшсл", "кик", "изгнать"],
		description="**Модераторская команда.** Кикает указанного пользователя.",
		usage="`/kick <пользователь> [причина]`",
		help="")
	@commands.has_permissions(kick_members=True)
	@app_commands.default_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, *, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.kick(reason=reason)
		embed = discord.Embed(title=f"{Emojis.door}Кик", color=no_color)
		embed.set_thumbnail(url=user.display_avatar.url)
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
		