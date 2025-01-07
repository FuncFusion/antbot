from discord.ext import commands
from settings import CHAT_ID
from utils.shortcuts import no_ping
from asyncio import sleep
from random import choice

else_dead_chat_msgs = {
    "Эээ это моя работа",
    "Ну йомайо теперь снова ждать",
    "Та блин я так долго сидел ждал",
    "э",
    "та ну что ж такое",
    "хватит за меня отправлять",
    "ну когда уже я смогу отправить"
}

class DeadChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def dead_chat(self, msg):
        if msg.channel.id != CHAT_ID:
            return
        if msg.author.bot:
            return
        if msg.created_at.hour >= 0 and msg.created_at.hour < 5:
            return
        new_message_id = msg.id
        if "https://tenor.com/view/ultra-dead-chat-dead-chat-gif-27600164" in msg.content.lower():
            await msg.reply(choice(list(else_dead_chat_msgs)), allowed_mentions=no_ping)

        await sleep(4*60*60)
        latest_messages = [msg async for msg in msg.channel.history(limit=1)]
        if latest_messages[0].id == new_message_id:
            await msg.channel.send("https://tenor.com/view/ultra-dead-chat-dead-chat-gif-27600164")