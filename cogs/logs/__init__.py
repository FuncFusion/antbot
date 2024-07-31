import discord
from discord.ext import commands
from discord.utils import MISSING

from settings import LOGS_CHANNEL_ID, DMS_LOGS_GUILD_ID, GUILD
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color
from utils.fake_user import fake_send
from utils.users_db import DB

class Logs(commands.Cog, name="no_help_logs"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener(name="on_message_edit")
	async def edited(self, before, after):
		if after.guild.id != GUILD:return
		if after.author.id != self.bot.user.id and before.content != after.content\
		and not isinstance(after.channel, discord.DMChannel):
			# Build ebmed
			embed = discord.Embed(title=f"{Emojis.edited_msg} Сообщение отредактировано", color=no_color)
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
		if msg.guild.id != GUILD:return
		if msg.author.id != self.bot.user.id and not isinstance(msg.channel, discord.DMChannel):
			# Getting files from message
			if msg.attachments != None:
				files = []
				for attachment in msg.attachments:
					files.append(await attachment.to_file())
			else:
				files = MISSING
			# Build ebmed
			embed = discord.Embed(title=f"{Emojis.deleted_msg} Сообщение удалено", color=no_color)
			embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
			embed.add_field(name="Автор", value=msg.author.mention)
			embed.add_field(name="Канал", value=msg.channel.jump_url)
			embed.add_field(name="Содержимое", value=msg.content[:1021] + ("..." if len(msg.content) >= 1024 else ""), inline=False)
			#
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(embed=embed, files=files)
	
	#dms
	@commands.Cog.listener(name="on_message")
	async def dms(self, msg):
		true_channel = await self.bot.fetch_channel(msg.channel.id) # It also triggers by ephemeral msgs so
		if isinstance(true_channel, discord.DMChannel):
			dm_author_id = true_channel.recipient.id
			dm_log_channel = await DB.DMs.get_channel(dm_author_id, self.bot)
			await fake_send(msg.author, dm_log_channel, msg.content, msg.attachments, msg.embeds)
	
	@commands.Cog.listener(name="on_message")
	async def send2dms(self, msg):
		if msg.guild != None and msg.guild.id == DMS_LOGS_GUILD_ID and not msg.author.bot:
			target_user = await self.bot.fetch_user(int(msg.channel.topic))
			if msg.attachments != None:
				files = []
				for attachment in msg.attachments:
					files.append(await attachment.to_file())
			else:
				files = MISSING
			await target_user.send(msg.content, files=files)


class JumpMessage(discord.ui.View):
	def __init__(self, msg_link):
		super().__init__()
		self.add_item(discord.ui.Button(
			label="Перейти к сообщению",
			emoji=f"{Emojis.link}",
			url=msg_link
		))
