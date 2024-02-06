import discord
from discord.ext import commands
from discord import app_commands

import asyncio

from settings import LOGS_CHANNEL_ID
from utils.shortcuts import no_ping, no_color

class LogListeners(commands.Cog, name="no_help_logs"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener(name="on_message_edit")
	async def edited(self, before, after):
		if after.author.id != self.bot.user.id and not isinstance(after.channel, discord.DMChannel):
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
		if msg.author.id != self.bot.user.id and isinstance(msg.channel, discord.DMChannel):
			# Build embed
			embed = discord.Embed(color=no_color, description=msg.content)
			embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
			#
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(embed=embed)


class JumpMessage(discord.ui.View):
	def __init__(self, msg_link):
		super().__init__()
		self.add_item(discord.ui.Button(
			label="Перейти к сообщению",
			emoji="↗️",
			url=msg_link
		))
