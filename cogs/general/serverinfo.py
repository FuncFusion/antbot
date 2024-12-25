import discord
from discord.ext import commands

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping


class ServerInfoCommand(commands.Cog):
	@commands.hybrid_command(name="server-info",
		aliases=["info", "server", "si", "сервер-инфо", "инфо", "сервер", "си", "ыукмукштащ", "штащ", "ыукмук", "ыш"],
		description="Показывает информацию о сервере.",
		usage="`/server-info`",
		help="")

	async def serverinfo(self, ctx):
		# setup vars
		server = ctx.guild
		if server is None:
			raise Exception("dm")
		member_count = 0
		bot_count = 0
		for member in server.members:
			if member.bot:
				bot_count += 1
			else:
				member_count += 1
		embed = discord.Embed(title=server.name, color=server.owner.color)
		embed.set_thumbnail(url=server.icon.url)
		embed.add_field(name="Владелец", value=f"{Emojis.crown} <@{server.owner_id}>", inline=False)
		embed.add_field(name="Сервер создан", value=f"{Emojis.calendar} <t:{int(server.created_at.timestamp())}>", inline=False)
		embed.add_field(name="Участники", value=f"{Emojis.users} {member_count} • {Emojis.bot} {bot_count}", inline=False)
		embed.add_field(name="Каналы", value=f"{Emojis.text_channel} {len(server.text_channels)} • {Emojis.speaker} {len(server.voice_channels)} • {Emojis.chat_type_file} {len(server.forums)}", inline=False)
		embed.add_field(name="Роли", value=f"{Emojis.role} {len(server.roles)}", inline=False)
		embed.add_field(name="Приглашение", value=f"{Emojis.link} https://discord.gg/anthill-914772142300749854")
		embed.set_footer(text=f"🆔 {server.id}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@serverinfo.error
	async def si_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "dm",
				"msg": "Эта команда работает только на серверах" 
			}
		])
	