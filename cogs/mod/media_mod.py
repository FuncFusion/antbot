import discord
from discord.ext import commands
from discord import app_commands
from settings import MEDIA_CHANNEL_ID

class MediaModeration(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_message")
	async def media_moderation(self, msg):
		if msg.channel.id != MEDIA_CHANNEL_ID:
			return
		if msg.author.bot:
			return
		if msg.attachments != [] or "https://" in msg.content or "http://" in msg.content:
			thread_name = msg.content[:97] if msg.content != "" else f"Обсуждение медиа {msg.author.display_name}"
			if len(msg.content) >= 100:
				thread_name + "..."
			await msg.create_thread(name=thread_name)
		else:
			await msg.delete()
			await msg.channel.send(f"{msg.author.mention} Обсуждайте в ветках!", delete_after=3)