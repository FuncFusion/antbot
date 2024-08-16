import discord
from discord import app_commands
from discord.ext import commands, tasks

from Levenshtein import distance
from collections import OrderedDict as odict
from json import dumps, loads
from pymongo import MongoClient

from settings import MONGO_URI
from utils.msg_utils import Emojis
from utils.packmcmeta import versions
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.misc


class PackformatCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format у дп и рп.",
		usage="`/packformat [все|версия майна]`",
		help="Если не вводить никаких аргументов, команда выдаст числа для последних нескольких версий игры. Если ввести определённую версию, выдаст именно для неё числа, а если `все` или `all`, то выдаст числа на все релизные версии.\n### Пример:\n`/packformat 1.21`")
	@app_commands.describe(version="Интересующая версия (так же можно указать 'все')")

	async def packformat(self, ctx, *, version: str=None):
		def format_table(versions, pack):
			return "\n".join([f"`{ver}` - `{versions[ver][pack]}`" for ver in versions])
		#
		version = None if not version else version.replace(" ", ".")
		if version in ("all", "al", "a", "все", "вс", "в", "фдд", "фд", "ф"):
			all_releases = {ver: versions[ver] for ver in versions if versions[ver]["type"]=="release"}
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Все версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпаки", value=format_table(all_releases, "data_pack"))
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспаки", value=format_table(all_releases, "resource_pack"))
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		elif version:
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Пакформат для {version}", color=no_color)
			try:
				dp_ver = f"`{versions[version]["data_pack"]}`"
			except:
				dp_ver = f"`-`"
			embed.add_field(name=f"{Emojis.deta_rack} Датaпак", value=dp_ver)
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспак", value=f"`{versions[version]["resource_pack"]}`")
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		else:
			all_releases = {ver: versions[ver] for ver in versions if versions[ver]["type"]=="release"}
			latest_releases = dict(tuple(all_releases.items())[:5])
			embed = discord.Embed(description=f"## {Emojis.pack_mcmeta} Последние версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.deta_rack} Датaпаки", value=format_table(latest_releases, "data_pack"))
			embed.add_field(name=f"{Emojis.resource_rack} Ресурспаки", value=format_table(latest_releases, "data_pack"))
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		print(error)
		await handle_errors(ctx, error, [])

