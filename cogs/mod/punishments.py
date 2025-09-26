import discord
from discord.ext import commands
from discord import app_commands, ui

from re import findall
from random import choice
from typing import Union
from datetime import timedelta

from utils import handle_errors, Emojis, no_ping, get_secs, LazyLayout

from time import time


def generate_stupid_reason():
    return choice([
        "Настолько жалок, что даже не достоин причины",
        "Ты хочешь показать всем свою неадекватность? Опозорится самому, опозорить честь сервера?",
        "Короче: читы — бан; кемперство — бан; оскорбление — бан; оскорбление администрации — расстрел, а потом бан",
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
		aliases=["ифт", "бан", "банчек", "заблокировать","забанить","кастую-бан"],
		description="**Модераторская команда.** Банит указанного пользователя.",
		usage="`/ban <пользователь> [причина]`",
		help="")
	@commands.has_permissions(ban_members=True)
	@app_commands.default_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.ban(reason=reason)
		#
		await ctx.reply(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.ban} Бан\n"
					f"**Забаненый участник**\n{user.name}({user.mention})\n"
					f"**Причина**\n{reason}",
					accessory=ui.Thumbnail(user.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)
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
			}
		])
	
	@commands.hybrid_command(
		aliases=["гтиат", "анбан", "разблокировать", "pardon", "разбанить", "пардон"],
		description="**Модераторская команда.** Разбанивает указанного пользователя.",
		usage="`/unban <пользователь>`",
		help="")
	@commands.has_permissions(ban_members=True)
	@app_commands.default_permissions(ban_members=True)
	async def unban(self, ctx, user: Union[discord.Member, discord.User]):
		await ctx.guild.unban(user)
		await ctx.reply(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.ban} Разбан\n"
					f"**Разабаненый участник**\n{user.name}({user.mention})",
					accessory=ui.Thumbnail(user.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)
	@unban.error
	async def unban_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите пользователя"
			},
			{
				"contains": "Unknown Ban",
				"msg": "Этот пользователь не забанен"
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
		final_term = min(get_secs(term), 2419200)
		reason = reason if reason != None else generate_stupid_reason()
		await user.timeout(timedelta(seconds=final_term), reason=reason)
		#
		await ctx.reply(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.mute} Мут\n"
					f"**Замученый участник**\n{user.mention}\n"
					f"**Замучен до**\n<t:{int(time()) + final_term}:R>\n"
					f"**Причина**\n{reason}",
					accessory=ui.Thumbnail(user.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)
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
		aliases=["гтьгеу", "анмут", "размут", "открыть-рот"],
		descripion="**Модератроская команда.** Снимает мут с указанного пользователя",
		usage="`/unmute <пользователь>`",
		help=""
	)
	@commands.has_permissions(moderate_members=True)
	@app_commands.default_permissions(moderate_members=True)
	async def unmute(self, ctx, member: discord.Member):
		if not member.is_timed_out():
			raise Exception("Not muted")
		await member.timeout(None)

		await ctx.reply(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.speaker} Размут\n"
					f"**Размученый участник**\n{member.mention}\n",
					accessory=ui.Thumbnail(member.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)

	@unmute.error
	async def unmute_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Not muted",
				"msg": "Пользователь и так не в муте"
			},
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Укажите пользователя"
			},
			{
				"exception": commands.MemberNotFound,
				"msg": "Пользователь не найден"
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
		help=""
	)
	@commands.has_permissions(kick_members=True)
	@app_commands.default_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, *, reason: str=None):
		reason = reason if reason != None else generate_stupid_reason()
		await user.kick(reason=reason)
		await ctx.reply(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.door} Кик\n"
					f"**Кикнутый участник**\n{user.name}({user.mention})\n"
					f"**Причина**\n{reason}",
					accessory=ui.Thumbnail(user.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)

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
		