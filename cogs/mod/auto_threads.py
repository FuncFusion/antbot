import discord
from discord.ext import commands
from discord import app_commands
from settings import MEDIA_CHANNEL_ID, FB_IDEAS_CHANNEL_ID
from re import sub

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
	content = sub(r"https?:\/\/\S+", "", msg.content)
	thread_name = content[:97]
	if len(thread_name) == 97:
		thread_name += "..."
	try:
		await msg.create_thread(name=thread_name)
	except discord.errors.HTTPException:
		channel_name = sub(r"[^\w-]*", "", msg.channel.name)
		await msg.create_thread(name=f"Обсуждение {channel_name} {msg.author.display_name}")
		