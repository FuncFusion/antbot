from discord.ext import commands
from settings import CHAT_ID
from utils.shortcuts import no_ping
from asyncio import sleep
from random import choice
from re import compile

dead_chat_link_re = compile(r"https://tenor\.com/view/[^ ]*dead[^ ]*chat[^ ]*")


dead_chat_gifs = [
    "https://tenor.com/view/dead-chat-dead-chat-skeleton-gif-25954239",
    "https://tenor.com/view/dead-chat-gif-26094097",
    "https://tenor.com/view/dead-group-chat-gif-23637113",
    "https://tenor.com/view/minecraft-dead-chat-dead-chat-xd-gif-24629150"
]

else_dead_chat_msgs = [
    "Эээ это моя работа",
    "Ну йомайо теперь снова ждать",
    "Та блин я так долго сидел ждал",
    "э",
    "та ну что ж такое",
    "хватит за меня отправлять",
    "ну когда уже я смогу отправить"
]

class DeadChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def dead_chat(self, msg):
        if msg.channel.id != CHAT_ID:
            return
        if msg.author.bot:
            return
        current_time = msg.created_at.replace(hour=(msg.created_at.hour + 4) % 24)
        if current_time.hour >= 0 and current_time.hour < 5:
            return
        new_message_id = msg.id
        if dead_chat_link_re.search(msg.content.lower()):
            await msg.reply(choice(else_dead_chat_msgs), allowed_mentions=no_ping)

        await sleep(4*60*60)
        latest_messages = [msg async for msg in msg.channel.history(limit=1)]
        if latest_messages[0].id == new_message_id:
            await msg.channel.send(choice(dead_chat_gifs))