import discord
from discord.ext import commands
from discord import app_commands
import re
import requests
from Levenshtein import distance
from bs4 import BeautifulSoup

from utils.emojis import Emojis
from utils.highlighter.main import Highlighter as hl
from utils.fake_user import fake_send
from utils.shortcuts import no_ping, no_color
from utils.msg_utils import unknown_error
from utils.msg_utils import get_msg_by_id_arg

code_block_content_re = r"```[a-zA-Z+]+\n|```\n?"

## Getting pack formats
pf_req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
pf_content = BeautifulSoup(pf_req.content, "html.parser")

class MinecraftCommands(commands.Cog, name="Майнкрафт"):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["hl", "рд","хайлайт", "хл"],
							description="Подсвечивает синтаксис для mcfunction")
		async def highlight(ctx, *, command:str=None):
			# Setting up vars
			message = ""
			if command == None:
				if (reply:=ctx.message.reference) != None:
					reply_message = await ctx.channel.fetch_message(reply.message_id)
					reply_message = reply_message.content
					if "```" in reply_message:
						for code_block in re.split(code_block_content_re, reply_message)[1::2]:
							message += f"```ansi\n{hl.highlight(code_block)}```"
					else:
						message += f"```ansi\n{hl.highlight(reply_message)}```"
				else:
					raise Exception("Missing arg")
			else:
				if "```" in command:
					for code_block in re.split(code_block_content_re, command)[1::2]:
						message += f"```ansi\n{hl.highlight(code_block)}```"
				else:
					message += f"```ansi\n{hl.highlight(command)}```"
			# Building embed
			embed = discord.Embed(title=f"{Emojis.sparkles} Подсвеченная функция" if message.count("```") == 2 else "Подсвеченные функции", color=no_color, description=message)
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		@highlight.error
		async def hl_error(ctx, error):
			error_msg = str(error)
			if "Missing arg" in error_msg:
				await ctx.reply("❗ Не хватает функции/ответа на сообщение с функцией", allowed_mentions=no_ping)
	
		@bot.tree.context_menu(name=f"🌈Подсветить функцию")
		async def highlight_ctxmenu(interaction: discord.Interaction, message:discord.Message):
			# Setting up variables
			code_block_re = r"```[^`]+```"
			if interaction.user == message.author:
				mcfed_message = " " + message.content
				if "```" in message.content:
					for code_block, code_block_content in zip(re.findall(code_block_re, message.content), re.split(code_block_content_re, message.content)[1::2]):
						mcfed_message = mcfed_message.replace(code_block, f"```ansi\n{hl.highlight(code_block_content)}```")
				else:
					mcfed_message = f"```ansi\n{hl.highlight(message.content)}```"
				await fake_send(interaction.user, interaction.channel, content=mcfed_message)
				await interaction.response.send_message(f"{Emojis.sparkles} Сообщение с функцией подсвечено", ephemeral=True)
				await message.delete()
			else:
				mcfed_message = ""
				if "```" in message.content:
					for code_block in re.split(code_block_content_re, message.content)[1::2]:
						mcfed_message += f"```ansi\n{hl.highlight(code_block)}```"
				else:
					mcfed_message += f"```ansi\n{hl.highlight(message.content)}```"
				# Building embed
				embed = discord.Embed(title=f"{Emojis.sparkles} Подсвеченная функция" if message.content.count("```") == 2 else "Подсвеченные функции", color=no_color, description=mcfed_message)
				await interaction.response.send_message(embed=embed)

		@bot.hybrid_command(aliases=["mcmetaformat","pack-format","pack_format",
							   "packmcmetaformat","pf","пакформат","пак-формат",
							   "пак_формат", "мсметаформат", "пакмсметаформат",
							   "пф", "зфслащкьфе", "за"], description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format")
		@app_commands.describe(type="Показать числа для ресурспака или датапака", show_all="Показать числа для всех версий и снапшотов")
		async def packformat(ctx, type, *, show_all=""):			
			dp_types = ["datapack", "dp", "data", "датапак", "дп", "дата"]
			rp_types = ["resourcepack", "rp", "resource", "ресурспак", "рп", "ресурс"]
			table, title, desc = None, "", ""
			for arg in rp_types:
				if distance(type, arg) <= round(len(arg))/3:
					title = f"{Emojis.pack_mcmeta2} Список чисел `pack_format` у ресурспака"
					table = pf_content.find("tbody")
			if table == None:
				for arg in dp_types:
					if distance(type, arg) <= round(len(arg))/3:
						title = f"{Emojis.pack_mcmeta2} Список чисел `pack_format` у датапака"
						table = pf_content.find_all("table")[1]
			for row in table.find_all("tr"):
					cells = row.find_all("td")
					if len(cells) >= 2:
						num = cells[0].get_text()
						version = cells[1].get_text()
						release = cells[2].get_text()
						if show_all != "":
							title = title.replace("С", "Полный с")
							desc += f"`{num}` — `{version}`\n"
						else:
							if release != "–":
								desc += f"`{num}` — `{release}`\n"
			embed = discord.Embed(title=title, color=no_color)
			embed.add_field(name="Число — Версии", value=desc)
			await ctx.reply(embed=embed, allowed_mentions=no_ping)
		@packformat.error
		async def packformat_error(ctx, error: Exception):
			error_msg = str(error)
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply("❗ Не хватает аргументов.", allowed_mentions=no_ping)
			elif error_msg.find("AttributeError"):
				await ctx.reply("❗ Неверно указан тип пакформата", allowed_mentions=no_ping)
			else:
				await unknown_error(ctx, error)