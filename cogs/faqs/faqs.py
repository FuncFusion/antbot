import discord
from discord.ext import commands
from discord import app_commands
import re
import json
from Levenshtein import distance
from utils.emojis import Emojis

with open("cogs/faqs/faqs.json", 'r', encoding="utf-8") as file: db = json.load(file)
faq_names = sorted(list(db.keys()))
faq_list = list(db.keys())
for value in db.values():
    faq_list.extend(value.get('aliases', []))

class FAQs(commands.Cog, name="Факьюшки"):
    def __init__(self, bot):

        @bot.hybrid_command(aliases=["факьюшки","вопросы-и-ответы","вопросыиответы", "вопросыответы","афйы"],
                            description = "Показывает список всех факьюшек/алиасов к определённой факьюшке")
        @app_commands.describe(name = "Название факьюшки, алиасы которого вы хотите посмотреть")
        async def faqs(ctx, *, name=None):
            embed = discord.Embed(color=discord.Colour.dark_embed())
            if name == None:
                faqs_str = ", ".join([f"`{faq}`" for faq in faq_names])
                embed.title = f"{Emojis.no_dp_icons} Список всех факьюшек"
                embed.add_field(name="", value=faqs_str, inline=False)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="Как использовать факьюшки?", value="Чтобы вызвать ответ на какую либо факьюшку, напишите вопросительный знак и после него название факьюшки. Вы также можете вызвать факьюшку всередине сообщения, сделав вопросительный знак жирным. Примеры:\n`?логи`\n`Тебе стоит открыть **?**логи, потому что в нём полезная инфа`")
                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
            else:
                faq = get_faq(name)
                aliases = ", ".join([f"`{alias}`" for alias in db[faq]['aliases']])             
                embed.title = f"{Emojis.txt} Список алиасов для \"{faq}\""
                embed.add_field(name="", value=aliases, inline=False)
                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())

        @bot.listen("on_message")
        async def main(msg):
            if msg.author == bot.user:
                return
            segments = re.findall(r'(?:^\?|\*\*\?\*\*)([^?*]+)(?:\*\*\?\*\*)*?', msg.content)
            if segments == []:
                return
            args = []
            for segment in segments:
                words = re.findall(r'\S+', segment)
                for i in range(len(words)):
                    args.append(' '.join(words[:i+1]))
            faq_names = []
            for arg in args:
                faq_name = get_faq(arg)
                if faq_name != None and faq_name not in faq_names:
                    faq_names.append(faq_name)
            if len(faq_names) > 3:
                await msg.channel.send(f"{Emojis.chat_type_open} Чтобы предотвратить флуд, я не буду отправлять больше трёх ответов за раз.", reference = msg, allowed_mentions = discord.AllowedMentions.none())
            for faq in faq_names:
                if faq_names.index(faq) < 3:
                    file_names = db[faq]["files"]
                    files = []
                    for file_name in file_names:
                        files.append(discord.File(f'assets/faqs/{faq}/{file_name}'))
                    with open(f'assets/faqs/{faq}/{faq}.md', 'r', encoding="utf-8") as file: answer = file.read()
                    emoji_instance = Emojis()
                    for attr in dir(emoji_instance):
                        if not attr.startswith("__") and not callable(getattr(emoji_instance, attr)):
                            answer = answer.replace("{" + attr + "}", getattr(emoji_instance, attr))
                    
                    await msg.channel.send(answer, files = files, reference = msg, allowed_mentions = discord.AllowedMentions.none())
                        
def get_faq(arg):
    for faq in faq_list:
        if distance(arg, faq) <= len(faq)/3:
            if faq not in faq_names:
                return get_root_obj(faq)
            else:
                return faq

def get_root_obj(alias):
    for key, value in db.items():
        if alias in value.get("aliases",[]):
            return key
    return None