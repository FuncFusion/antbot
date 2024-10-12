import discord
from discord.ext import commands
from discord import app_commands
from settings import MEDIA_CHANNEL_ID, FB_IDEAS_CHANNEL_ID

class AutoThreads(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_message")
	async def auto_threads(self, msg):
		if msg.channel.id != MEDIA_CHANNEL_ID and msg.channel.id != FB_IDEAS_CHANNEL_ID:
			return
		if msg.author.bot:
			return
		if msg.channel.id == FB_IDEAS_CHANNEL_ID and "https://discord.com/channels/1138536747932864532" in msg.content:
			print("hi")
			await create_auto_thread(msg) 
		elif msg.channel.id == MEDIA_CHANNEL_ID and (msg.attachments != [] or "https://" in msg.content or "http://" in msg.content):
			print(msg.channel.id == MEDIA_CHANNEL_ID) 
			await create_auto_thread(msg)
		else:
			await msg.delete()
			await msg.channel.send(f"{msg.author.mention} Обсуждайте в ветках!", delete_after=3)
	
async def create_auto_thread(msg):
	thread_name = msg.content[:97] if msg.content != "" else f"Обсуждение медиа {msg.author.display_name}"
	if len(msg.content) >= 100:
		thread_name += "..."
	await msg.create_thread(name=thread_name)