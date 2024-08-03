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
from utils.validator import validate

db = MongoClient(MONGO_URI).antbot.misc

pf_req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
pf_content = BeautifulSoup(pf_req.content, "html.parser")


class PackformatCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.get_latest_mcmeta.start()
	
	@tasks.loop(minutes=40)
	async def get_latest_mcmeta(self):
		req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
		content = BeautifulSoup(pf_req.content, "html.parser")
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
						versions["releases_"+pack][rel.replace(" ", "")] = num
					for snap in snapshot.split("–"):
						versions[pack][snap.replace(" ", "")] = num
		db.update_one({"_id": "latest_mcmeta"}, {"$set": {"_": dumps(versions)}})

	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "pack_format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", "пак_формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format")
	@app_commands.describe(version="Интересующая версия (так же можно указать 'все')")

	async def packformat(self, ctx, *, version: str=None):
		versions = odict(loads(db.find_one({"_id": "latest_mcmeta"})["_"]))
		if version in ("all", "a", "в", "все"):
			version = version.replace(" ", ".")
		elif version:
			version = validate(version, versions)
			embed = discord.Embed(title=f"{Emojis.pack_mcmeta} Пакформат для {version}", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпак", value=versions["dp"][version])
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспак", value=versions["rp"][version])
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		else:
			embed = discord.Embed(title=f"{Emojis.pack_mcmeta} Последние версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпаки", value="\n".join([f"{'\u2002'*(6-len(i))}{i} - {j}" for i, j in \
				list(versions["releases_dp"].items())[-5:]]))
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспаки", value="\n".join([f"{'\u2002'*(6-len(i))}{i} - {j}" for i, j \
				in list(versions["releases_rp"].items())[-5:]]))
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов"
			},
			{
				"contains": "AttributeError",
				"msg": "Неверно указан тип пакформата"
			}
		])

