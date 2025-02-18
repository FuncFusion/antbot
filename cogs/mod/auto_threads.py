import discord
from discord.ext import commands

from settings import MEDIA_CHANNEL_ID, FB_IDEAS_CHANNEL_ID
from asyncio import sleep
from re import sub


class AutoThreads(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.waiting_for_forward_comment = False

	@commands.Cog.listener("on_message")
	async def auto_threads(self, msg):
		if msg.channel.id != MEDIA_CHANNEL_ID and msg.channel.id != FB_IDEAS_CHANNEL_ID:
			return
		if msg.author.bot:
			return
		if msg.channel.id == FB_IDEAS_CHANNEL_ID and "https://discord.com/channels/1138536747932864532" in msg.content:
			await create_auto_thread(msg) 
		if msg.channel.id == MEDIA_CHANNEL_ID:
			if (msg.attachments != [] or "https://" in msg.content or "http://" in msg.content):
				await create_auto_thread(msg)
			elif msg.flags.forwarded:
				self.waiting_for_forward_comment = True
				await self.handle_forward(msg)
			elif not self.waiting_for_forward_comment:
				await msg.delete()
				await msg.channel.send(f"{msg.author.mention} Обсуждайте в ветках!", delete_after=3)
		else:
			await msg.delete()
			await msg.channel.send(f"{msg.author.mention} Обсуждайте в ветках!", delete_after=3)
	
	async def handle_forward(self, msg):
		end_msg = msg
		msg_content = msg.message_snapshots[0].content
		await sleep(0.7)
		self.waiting_for_forward_comment = False
		if msg.channel.last_message_id != msg.id:
			end_msg = await msg.channel.fetch_message(msg.channel.last_message_id)
			if not msg_content:
				msg_content = end_msg.content
		await create_auto_thread(end_msg, msg_content)


async def create_auto_thread(msg, msg_content=None):
	msg_content = msg_content if msg_content else msg.content
	content = sub(r"https?:\/\/\S+", "", msg_content)
	thread_name = content[:97]
	if len(thread_name) == 97:
		thread_name += "..."
	try:
		await msg.create_thread(name=thread_name)
	except discord.errors.HTTPException:
		channel_name = sub(r"[^\w-]*", "", msg.channel.name)
		await msg.create_thread(name=f"Обсуждение {channel_name} {msg.author.display_name}")
