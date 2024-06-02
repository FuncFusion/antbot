import discord
from discord.ext import commands
from discord import app_commands

from typing import List
from math import ceil
import re
import requests
from Levenshtein import distance
from bs4 import BeautifulSoup

from cogs.mc.pack_generator import PGenerator, Modals
from cogs.mc.highlighter.main import Hl as hl

from utils.general import handle_errors
from utils.validator import validate
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color
from utils.fake_user import fake_send
from utils.msg_utils import unknown_error
from utils.tree_gen import generate_tree

code_block_content_re = r"```[a-zA-Z+]+\n|```\n?"

pf_req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
pf_content = BeautifulSoup(pf_req.content, "html.parser")

class MinecraftCommands(commands.Cog, name="Майнкрафт"):
	def __init__(self, bot):
		self.bot = bot
		self.bot.tree.add_command(app_commands.ContextMenu(
			name="🌈Подсветить функцию",
			callback=self.highlight_ctxmenu
		))

	@commands.hybrid_command(aliases=["hl", "рд","хайлайт", "хл"], description="Подсвечивает синтаксис для mcfunction")
	@app_commands.describe(function="mcfunction функция")
	async def highlight(self, ctx, *, function:str=None):
		highlighted = ""
		if function == None:
			if (reply:=ctx.message.reference) != None:
				reply_message = await ctx.channel.fetch_message(reply.message_id)
				reply_message = reply_message.content
				if "```" in reply_message:
					for code_block in re.split(code_block_content_re, reply_message)[1::2]:
						highlighted += f"```ansi\n{hl.highlight(code_block)}```"
				else:
					highlighted += f"```ansi\n{hl.highlight(reply_message)}```"
			else:
				raise Exception("Missing arg")
		else:
			if "```" in function:
				for code_block in re.split(code_block_content_re, function)[1::2]:
					highlighted += f"```ansi\n{hl.highlight(code_block)}```"
			else:
				highlighted += f"```ansi\n{hl.highlight(function)}```"
		await ctx.reply(content=highlighted, allowed_mentions=no_ping)
	@highlight.error
	async def hl_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Missing arg",
				"msg": "{Emojis.exclamation_mark} Не хватает функции/ответа на сообщение с функцией"
			}
		])
	
	async def highlight_ctxmenu(self, interaction: discord.Interaction, message:discord.Message):
		code_block_re = r"```[^`]+```"
		if interaction.user == message.author:
			highlighted = " " + message.content
			await interaction.response.send_message(f"{Emojis.sparkles} Сообщение с функцией подсвечено", ephemeral=True)
			await message.delete()
			if "```" in message.content:
				for code_block, code_block_content in zip(re.findall(code_block_re, message.content), \
					re.split(code_block_content_re, message.content)[1::2]):
					highlighted = highlighted.replace(code_block, f"```ansi\n{hl.highlight(code_block_content)}```")
			else:
				highlighted = f"```ansi\n{hl.highlight(message.content)}```"
			if (hl_len:=len(highlighted)) > 2000:
				highlighted = hl.split_msg(highlighted)
				print(highlighted)
			await fake_send(interaction.user, interaction.channel, content=highlighted)
		else:
			highlighted = ""
			if "```" in message.content:
				for code_block in re.split(code_block_content_re, message.content)[1::2]:
					highlighted += f"```ansi\n{hl.highlight(code_block)}```"
			else:
				highlighted += f"```ansi\n{hl.highlight(message.content)}```"
			# Building embed
			await interaction.response.send_message(content=highlighted)

	@commands.hybrid_command(aliases=["mcmetaformat","pack-format","pack_format",
		"packmcmetaformat","pf","пакформат","пак-формат",
		"пак_формат", "мсметаформат", "пакмсметаформат",
		"пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format")
	@app_commands.describe(type="Показать числа для ресурспака или датапака", 
		show_all="Показать числа для всех версий и снапшотов")
	async def packformat(self, ctx, type, *, show_all=""):			
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
							desc += f"`{num}` — `{release[:-1]}`\n"
		embed = discord.Embed(title=title, color=no_color)
		embed.add_field(name="Число — Версии", value=desc)
		embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Не хватает аргументов"
			},
			{
				"contains": "AttributeError",
				"msg": f"{Emojis.exclamation_mark} Неверно указан тип пакформата"
			}
		])
	
	@commands.hybrid_command(aliases=["tl", "темплейт", "тэмплейт", "еуьздфеу", "шаблон"],
		description="Создаёт шаблон датапака/ресурспака")
	@app_commands.describe(template="Датапак/ресусрпак", type="Тип пака")
	async def template(self, ctx: commands.Context, template: str="datapack", type: str="basic"):
		pack_ctx = {
			"datapack": {"emoji": Emojis.deta_rack, "accusative": "датапака", "modal": Modals.DP},
			"resourcepack": {"emoji": Emojis.resource_rack, "accusative": "ресурспака", "modal": Modals.RP}
		}
		#Validating args
		if (v_template:=validate(template, {"datapack": ["dp", "дп", "датапак", "детарак", "патадак"], "resourcepack": ["rp", "рп", "ресурспак", "репуксрак"]}))\
			!= None:
			template = v_template
		else:
			raise commands.BadArgument(template)
		if (v_type:=validate(type, {"basic": ["базовый", "стандартный", "обычный"], "extended": ["расширенный", "полный"], "custom": ["кастомынй", "настраиваемый"]}))\
			!= None:
			type = v_type
		else:
			raise commands.BadArgument(type)
		for arg in [template, type]:
			if arg == None:
				raise commands.BadArgument(f"{arg}")
		#
		if type == "custom":
			await ctx.interaction.response.send_modal(pack_ctx[template]["modal"]())
		elif type == "extended":
			with open(f"assets/templates/Extended {template}.zip", "rb") as pack:
				await ctx.send(f"{pack_ctx[template]["emoji"]} Расширенный шаблон {pack_ctx[template]["accusative"]}", 
				file=discord.File(pack, filename=f"Extended_{template}_(UNZIP).zip"))
		elif type == "basic":
			with open(f"assets/templates/Basic {template}.zip", "rb") as pack:
				await ctx.send(f"{pack_ctx[template]["emoji"]} Базовый шаблон {pack_ctx[template]["accusative"]}", 
				file=discord.File(pack, filename=f"Basic_{template}_(UNZIP).zip"))
	@template.error
	async def template_error(self, ctx: commands.Context, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Не хватает аргументов"
			},
			{
				"exception": commands.BadArgument,
				"msg": f"{Emojis.exclamation_mark} Неверный аргумент"
			}
		])
	@template.autocomplete("template")
	async def template_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return [app_commands.Choice(name="Датапак", value="datapack"), app_commands.Choice(name="Ресурспак", value="resourcepack")]
	@template.autocomplete("type")
	async def template_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return [app_commands.Choice(name="Базовый", value="basic"), app_commands.Choice(name="Расширенный", value="extended"),
		  app_commands.Choice(name="Настраиваемый", value="custom")]
	
