import discord
from discord import ui
from discord.ext import commands
from discord.utils import MISSING

from datetime import datetime, timedelta, timezone
from pymongo.mongo_client import MongoClient

from settings import LOGS_CHANNEL_ID, DMS_LOGS_GUILD_ID, GUILD, CREATE_VC_CHANNEL_ID, MONGO_URI
from utils import Emojis, no_color, no_ping, fake_send, DB, LazyLayout

command_statistics = MongoClient(MONGO_URI).antbot.command_statistics


class Logs(commands.Cog, name="no_help_logs"):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	
	@commands.Cog.listener(name="on_member_update")
	async def nick_changed(self, before: discord.Member, after: discord.Member):
		if after.guild.id == GUILD and before.nick != after.nick:
			
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(
				view=LazyLayout(
					ui.Section(
						f"# {Emojis.user} Ник обновлён\n"
						f"**Участник**\n{after.mention}\n"
						f"**До**\n{before.display_name}\n"
						f"**Поcле**\n{after.display_name}\n",
						accessory=ui.Thumbnail(after.display_avatar.url)
					)
				),
				allowed_mentions=no_ping
			)
	
	@commands.Cog.listener(name="on_voice_state_update")
	async def voice_event(self, member: discord.Member, before: discord.VoiceChannel, after: discord.VoiceChannel):
		if member.guild.id == GUILD:

			if before.channel != after.channel and after.channel != None and after.channel.id != CREATE_VC_CHANNEL_ID:
				text = (
					f"# {Emojis.vc_joined} Участник зашёл в гк\n"
					f"**Участник**\n{member.mention}\n"
					f"**Канал**\n{after.channel.name} ({after.channel.mention})"
				)

			elif not after.channel:
				text = (
					f"# {Emojis.vc_left} Участник покинул гк\n"
					f"**Участник**\n{member.mention}\n"
					f"**Канал**\n{before.channel.name} ({before.channel.mention})"
				)

			else:return
			#
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(
				view=LazyLayout(
					ui.Section(
						text,
						accessory=ui.Thumbnail(member.display_avatar.url)
					)
				),
				allowed_mentions=no_ping
			)
	
	@commands.Cog.listener(name="on_message_edit")
	async def edited(self, before: discord.Message, after: discord.Message):
		if after.guild and after.guild.id == GUILD and after.author.id != self.bot.user.id and before.content != after.content\
		and not isinstance(after.channel, discord.DMChannel):
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(
				view=LazyLayout(
					ui.Section(
						f"# {Emojis.edited_msg} Сообщение отредактировано\n"
						f"**Автор**\n{after.author.mention}",
						accessory=ui.Thumbnail(after.author.display_avatar.url)
					)
				),
				allowed_mentions=no_ping
			)
			await log_channel.send(view=LazyLayout(ui.TextDisplay(f"# До\n{before.content}")), allowed_mentions=no_ping)
			await log_channel.send(view=LazyLayout(ui.TextDisplay(f"# После\n{after.content}")), allowed_mentions=no_ping)

	@commands.Cog.listener(name="on_message_delete")
	async def deleted(self, msg: discord.Message):
		if msg.guild.id != GUILD:return
		if msg.author.id != self.bot.user.id and not isinstance(msg.channel, discord.DMChannel):
			# Getting files from message
			files = []
			media_gal = ui.MediaGallery()
			non_media = []
			if msg.attachments != None:
				for attachment in msg.attachments:
					files.append(await attachment.to_file())
					if attachment.content_type and any((i in attachment.content_type.lower() for i in ("video", "image"))):
						media_gal.add_item(media=f"attachment://{attachment.filename}")
					else:
						non_media.append(ui.File(f"attachment://{attachment.filename}"))
			attachment_items = []
			if media_gal.items:
				attachment_items.append(media_gal)
			if non_media:
				attachment_items += non_media
			# Deleter
			now = datetime.now(timezone.utc)
			deleter = msg.author.mention
			guild = await self.bot.fetch_guild(GUILD)
			async for entry in guild.audit_logs(limit=5):
				if entry.action == discord.AuditLogAction.message_delete and entry.target.id == msg.author.id and\
				abs(now - entry.created_at) <= timedelta(seconds=2):
					deleter = entry.user.mention
			# Build ebmed
			log_channel = await self.bot.fetch_channel(LOGS_CHANNEL_ID)
			await log_channel.send(
				view=LazyLayout(
					ui.Section(
						f"{Emojis.deleted_msg} Сообщение удалено\n"
						f"**Автор**\n{msg.author.mention}\n"
						f"**Удалитель**\n{deleter}\n"
						f"**Канал**\n{msg.channel.jump_url}\n",
						accessory=ui.Thumbnail(msg.author.display_avatar.url)
					)
				), 
				allowed_mentions=no_ping
			)
			await log_channel.send(
				view=LazyLayout(
					ui.TextDisplay(f"## Содержимое\n{msg.content}"),
					*attachment_items
				),
				files=files,
			)
	
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
	
	#commands usage
	@commands.Cog.listener(name="on_command")
	async def command_used(self, ctx):
		command_statistics.update_one({"_id": ctx.command.name}, {"$inc": {"uses": 1}}, upsert=True)


class JumpMessage(discord.ui.View):
	def __init__(self, msg_link):
		super().__init__()
		self.add_item(discord.ui.Button(
			label="Перейти к сообщению",
			emoji=f"{Emojis.link}",
			url=msg_link
		))
