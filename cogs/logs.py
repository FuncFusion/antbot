import discord
from discord.ext import commands
from discord import app_commands

import asyncio

from settings import LOGS_CHANNEL_ID, DMS_LOGS_GUILD_ID
from utils.shortcuts import no_ping, no_color
from utils.fake_user import fake_send
from utils.users_db import DB

class LogListeners(commands.Cog, name="no_help_logs"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener(name="on_message_edit")
	async def edited(self, before, after):
		if after.author.id != self.bot.user.id and before.content != after.content\
		and not isinstance(after.channel, discord.DMChannel):
			# Build ebmed
			embed = discord.Embed(title="📝 Сообщение отредактировано", color=no_color)
			embed.set_author(icon_url=after.author.avatar.url, name=after.author.name)
			embed.add_field(name="Автор", value=after.author.mention)
			embed.add_field(name="Канал", value=after.channel.jump_url)
			embed.add_field(name="До", value=before.content[:1021] + ("..." if len(before.content) >= 1024 else ""), 
				inline=False)
			embed.add_field(name="После", value=after.content[:1021] + ("..." if len(after.content) >= 1024 else ""), 
				inline=False)
			#
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(embed=embed, view=JumpMessage(after.jump_url))

	@commands.Cog.listener(name="on_message_delete")
	async def deleted(self, msg):
		if msg.author.id != self.bot.user.id and not isinstance(msg.channel, discord.DMChannel):
			# Getting files from message
			files = []
			for attachment in msg.attachments:
				files.append(await attachment.to_file())
			# Build ebmed
			embed = discord.Embed(title="🚫 Сообщение удалено", color=no_color)
			embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
			embed.add_field(name="Автор", value=msg.author.mention)
			embed.add_field(name="Канал", value=msg.channel.jump_url)
			embed.add_field(name="Содержимое", value=msg.content[:1021] + ("..." if len(msg.content) >= 1024 else ""), inline=False)
			#
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(embed=embed)
			await log_channel.send(files=files)
	
	#dms
	@commands.Cog.listener(name="on_message")
	async def dms(self, msg):
		if isinstance(msg.channel, discord.DMChannel):
			if msg.author == self.bot.user:
				async for dmmsg in msg.channel.history(limit=15):
					if dmmsg.author != self.bot.user:
						dm_author_id = dmmsg.author.id
						break
				dm_log_channel = await DB.DMs.get_channel(dm_author_id, self.bot)
			else:
				dm_log_channel = await DB.DMs.get_channel(msg.author.id, self.bot)
			print(msg.attachments)
			await fake_send(msg.author, dm_log_channel, msg.content, msg.attachments, msg.embeds)
	
	@commands.Cog.listener(name="on_message")
	async def send2dms(self, msg):
		if msg.guild != None and msg.guild.id == DMS_LOGS_GUILD_ID and not msg.author.bot:
			target_user = self.bot.get_user(int(msg.channel.topic))
			await target_user.send(msg.content)


class JumpMessage(discord.ui.View):
	def __init__(self, msg_link):
		super().__init__()
		self.add_item(discord.ui.Button(
			label="Перейти к сообщению",
			emoji="↗️",
			url=msg_link
		))
