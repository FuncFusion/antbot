import discord
from discord.ext import commands
from discord import app_commands

from Levenshtein import distance
import requests
from bs4 import BeautifulSoup

from utils.msg_utils import Emojis
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping


pf_req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
pf_content = BeautifulSoup(pf_req.content, "html.parser")


class PackformatCommand(commands.Cog):
	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "pack_format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", "пак_формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format")
	@app_commands.describe(type="Показать числа для ресурспака или датапака", 
		show_all="Показать числа для всех версий и снапшотов")

	async def packformat(self, ctx, type, show_all=""):
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

