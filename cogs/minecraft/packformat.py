import discord
from discord import app_commands
from discord.ext import commands, tasks

from Levenshtein import distance
from collections import OrderedDict as odict
from json import dumps, loads
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from settings import MONGO_URI
from utils.msg_utils import Emojis
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.misc


class PackformatCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.get_latest_mcmeta.start()
	
	@tasks.loop(minutes=40)
	async def get_latest_mcmeta(self):
		req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
		content = BeautifulSoup(req.content, "html.parser")
		tables = ((content.find_all("table")[1], "dp"), (content.find("tbody"), "rp"))
		versions = {"dp": odict(), "rp": odict(), "releases_dp": odict(), "releases_rp": odict()}
		for table, pack in tables:
			for row in table.find_all("tr"):
				cells = row.find_all("td")
				if len(cells) >= 2:
					num = cells[0].get_text()
					snapshot = cells[1].get_text()
					release = cells[2].get_text()
					for rel in release.split("–"):
						versions[pack][rel.replace(" ", "")] = num
						if release != "–":
							versions["releases_"+pack][release[:-1]] = num
					for snap in snapshot.split("–"):
						versions[pack][snap.replace(" ", "")] = num
		db.update_one({"_id": "latest_mcmeta"}, {"$set": {"_": dumps(versions)}})

	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format у дп и рп.",
		usage="`/packformat [все|версия майна]`",
		help="Если не вводить никаких аргументов, команда выдаст числа для последних нескольких версий игры. Если ввести определённую версию, выдаст именно для неё числа, а если `все` или `all`, то выдаст числа на все релизные версии.\n### Пример:\n`/packformat 1.21`")
	@app_commands.describe(version="Интересующая версия (так же можно указать 'все')")

	async def packformat(self, ctx, *, version: str=None):
		def format_table(table):
			return "\n".join([f"`{j}` - `{i}`" for i, j in table])
		#
		versions = loads(db.find_one({"_id": "latest_mcmeta"})["_"])
		version = None if not version else version.replace(" ", ".")
		if version in ("all", "al", "a", "все", "вс", "в", "фдд", "фд", "ф"):
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Все версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпаки", value=format_table(list(versions["releases_dp"].items())))
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспаки", value=format_table(list(versions["releases_rp"].items())))
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		elif version:
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Пакформат для {version}", color=no_color)
			try:
				dp_ver = f"`{versions["dp"][version]}`"
			except:
				dp_ver = f"`-`"
			embed.add_field(name=f"{Emojis.deta_rack} Датaпак", value=dp_ver)
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспак", value=f"`{versions["rp"][version]}`")
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		else:
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Последние версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпаки", value=format_table(list(versions["releases_dp"].items())[-5:]))
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспаки", value=format_table(list(versions["releases_rp"].items())[-5:]))
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"contains": "KeyError",
				"msg": "Неверно указана версия/версия находится в промежутке (см. в </packformat:1203447815305691206> `version:all`)"
			}
		])

