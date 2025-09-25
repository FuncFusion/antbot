import discord
from discord.ext import commands
from discord import app_commands

from settings import DMS_LOGS_GUILD_ID

from Levenshtein import distance
import re
import os
from typing import List
import json

from utils import handle_errors, Emojis, no_ping, all_valid, closest_match, LazyLayout


with open("cogs/faqs/faqs.json", 'r', encoding="utf-8") as file: db = json.load(file)
faq_names = sorted(list(db.keys()))

offered_faqs = [app_commands.Choice(name=faq, value=faq) for faq in faq_names[:25]]


class FAQs(commands.Cog, name="FAQ команды"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["faq","fqs","fs","qna","qnas","факьюшки","чаво","чавошки","вопросы-и-ответы","вопросыиответы", "вопросыответы","афйы","ф","факс"],
		description = "Показывает список всех факьюшек/алиасов к определённой факьюшке.",
		usage="`/faqs [название факьюшки]`",
		help="Смотрите `/help FAQшки` для получения большей информации о них.")
	@app_commands.describe(name = "Название факьюшки, алиасы которой вы хотите посмотреть")
	async def faqs(self, ctx, *, name=None):
		text = ""

		if name == None:
			faqs_str = ", ".join([f"`{faq}`" for faq in faq_names])
			text = str(
				f"## {Emojis.question_mark} Список всех факьюшек ({len(faq_names)}):\n{faqs_str}\n"
				"**Как использовать факьюшки?**\nЧтобы вызвать ответ на какую либо факьюшку, "
				"напишите вопросительный знак и после него название факьюшки. Вы также можете "
				"вызвать факьюшку всередине сообщения, сделав вопросительный знак жирным. "
				"Примеры:\n`?логи`\n`Тебе стоит открыть **?**логи, потому что в них полезная инфа`"
			)
		
		else:
			faq = closest_match(name, db, accuracy=3)
			aliases = ", ".join([f"`{alias}`" for alias in db[faq]])
			text = str(
				f"### {Emojis.txt} Список алиасов для \"{faq}\"\n"
				f"{aliases}\n\n"
				"-# Смотрите /help FAQшки для получения большей информации о них."
			)
		await ctx.reply(
			view=LazyLayout(
				discord.ui.TextDisplay(text)
			), 
			allowed_mentions=no_ping
		)
	
	@faqs.autocomplete(name="name")
	async def link_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_faqs
		if curr != "":
			return [app_commands.Choice(name=faq, value=faq) for faq in all_valid(curr, db)][:25]
		else:
			return offered_faqs
	
	@faqs.error
	async def faqs_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "KeyError",
				"msg": "Факьюшка по вашему запросу не найдена"
			}
		])

	@commands.Cog.listener("on_message")
	async def main(self, msg):
		if msg.author.bot:
			return
		if msg.guild != None and msg.guild.id == DMS_LOGS_GUILD_ID:
			return
		segments = re.findall(r'(?:^\?|\*\*\?\*\*)([^?*]+)(?:\*\*\?\*\*)*?', msg.content)
		if segments == []:
			return
		args = []
		for segment in segments:
			words = re.findall(r'\S+', segment)
			for i in range(len(words)):
				args.append(' '.join(words[:i+1]))
		faq = None
		for arg in args:
			faq_name = closest_match(arg, db, accuracy=3)
			if faq_name != None:
				faq = faq_name
		if faq == None:
			await handle_errors(msg, AttributeError("Not Found"), [{
				"exception": AttributeError,
				"msg": "Факьюшка не найдена"
			}])
			return
		files = []
		for filename in os.listdir(f"assets/faqs/{faq}"):
			if not filename.endswith(".md"):
				files.append(discord.File(f'assets/faqs/{faq}/{filename}'))
		with open(f'assets/faqs/{faq}/{faq}.md', 'r', encoding="utf-8") as file: content = file.read()
		emoji_instance = Emojis()
		for attr in dir(emoji_instance):
			if not attr.startswith("__") and not callable(getattr(emoji_instance, attr)):
				content = content.replace("{" + attr + "}", getattr(emoji_instance, attr))
		answers = content.split("\n---separator---\n")
		for answer in answers:
			if len(answers) == 1:
				#answer += "\n-# Источник: [AntBot](<https://github.com/FuncFusion/antbot>)"
				await msg.reply(answer, files=files, allowed_mentions=no_ping)
			elif answers.index(answer) == 0:
				await msg.reply(answer, allowed_mentions=no_ping)
			elif answer != answers[-1]:
				await msg.channel.send(answer, allowed_mentions=no_ping)
			else:
				#answer += "\n-# Источник: [AntBot](<https://github.com/FuncFusion/antbot>)"
				await msg.channel.send(answer, files=files, allowed_mentions=no_ping)
		
