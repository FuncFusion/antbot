from discord import Thread, Message
from discord.ui import TextDisplay

from re import compile

digit_regex = compile(r"\d+")

async def get_minecraft_version(thread: Thread):
    starter_message: Message = await thread.fetch_message(thread.id)
    content = starter_message.components[0].content
    version_line = content.split("Версия майнкрафта\n`")[-1].split("`")[0]
    digits = digit_regex.findall(version_line)
    version_normalised = ".".join(digits[:3])
    return version_normalised
