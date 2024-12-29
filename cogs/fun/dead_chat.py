from discord.ext import commands
from settings import CHAT_ID
from asyncio import sleep

class DeadChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def dead_chat(self, msg):
        if msg.channel.id != CHAT_ID:
            return
        if msg.author.bot:
            return
        new_message_id = msg.id
        await sleep(4*60*60)
        latest_messages = [msg async for msg in msg.channel.history(limit=1)]
        if latest_messages[0].id == new_message_id:
            await msg.channel.send("https://tenor.com/view/ultra-dead-chat-dead-chat-gif-27600164")