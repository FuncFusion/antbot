import discord
from discord.ext import commands

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping


class ServerInfoCommand(commands.Cog):
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

	@serverinfo.error
	async def si_error(self, ctx, error):
		await handle_errors(ctx, error, [])
	