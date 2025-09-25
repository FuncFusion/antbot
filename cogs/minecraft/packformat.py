import discord
from discord import app_commands
from discord.ext import commands, tasks

from Levenshtein import distance
from collections import OrderedDict as odict
from json import dumps, loads
from re import sub
from pymongo import MongoClient

from settings import MONGO_URI
from utils.msg_utils import Emojis
from utils.packmcmeta import get_mcmeta_ver
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.misc
offered_versions = (app_commands.Choice(name="Все", value="все"), app_commands.Choice(name="Последняя", value="последняя"))


class PackformatCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format у дп и рп.",
		usage="`/packformat [все|версия майна]`",
		help="Если не вводить никаких аргументов, команда выдаст числа для последних нескольких версий игры. Если ввести определённую версию, выдаст именно для неё числа, если `все`, то выдаст числа на все релизные версии, а если `последняя`, то выдаст числа для последней версии/снапшота.\n### Пример:\n`/packformat 1.21`")
	@app_commands.describe(version="Интересующая версия")

	async def packformat(self, ctx, *, version: str=None):
		versions = get_mcmeta_ver(requested_version="all")
		version = None if not version else version.replace(" ", ".")

		if version in ("all", "al", "a", "все", "вс", "в", "фдд", "фд", "ф"):
			all_releases = {ver: versions[ver] for ver in versions if versions[ver]["type"]=="release"}
			versions_formatted_dp = transform_version_data(all_releases, "data_pack")
			versions_formatted_rp = transform_version_data(all_releases, "resource_pack")
			embed = discord.Embed(description=f"## {Emojis.packformat} Все (релизные) версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.data_open} Датaпаки", value=versions_formatted_dp)
			embed.add_field(name=f"{Emojis.assets_open} Ресурспаки", value=versions_formatted_rp)
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")

		elif version:
			if version in ("latest","последняя","последний"):
				version = versions["latest"]["id"]
			embed = discord.Embed(description=f"## {Emojis.packformat} Пак формат для {version}", color=no_color)
			try:
				dp_ver = f"`{versions[version]["data_pack"]}`"
			except:
				dp_ver = f"`—`"
			embed.add_field(name=f"{Emojis.data_open} Датaпак", value=dp_ver)
			embed.add_field(name=f"{Emojis.assets_open} Ресурспак", value=f"`{versions[version]["resource_pack"]}`")
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")

		else:
			all_releases = {ver: versions[ver] for ver in versions if versions[ver]["type"]=="release"}
			versions_formatted_dp = versions_formatted_rp = ""
			if versions["latest"]["type"] == "snapshot":
				versions_formatted_dp += f"`{versions['latest']['data_pack']}` \u2500 `{versions['latest']['id']}`\n"
				versions_formatted_rp += f"`{versions['latest']['resource_pack']}` \u2500 `{versions['latest']['id']}`\n"
			versions_formatted_dp += "\n".join(transform_version_data(all_releases, "data_pack").split("\n")[:5])
			versions_formatted_rp += "\n".join(transform_version_data(all_releases, "resource_pack").split("\n")[:5])
			embed = discord.Embed(description=f"## {Emojis.packformat} Последние версии пак формата", color=no_color)
			embed.add_field(name=f"{Emojis.data_open} Датaпаки", value=versions_formatted_dp)
			embed.add_field(name=f"{Emojis.assets_open} Ресурспаки", value=versions_formatted_rp)
			embed.set_footer(text="Больше инфы в факьюшке \"?pack mcmeta\"")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	
	@packformat.autocomplete(name="version")
	async def file_autocomplete(self, ctx: discord.Interaction, curr: str):
		return offered_versions

	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"contains": "KeyError",
				"msg": "Пакформат для указанной версии не найден"
			}
		])

def transform_version_data(version_data, pack_type='data_pack'):
	grouped_versions = {}
	for version, data in version_data.items():
		pack_value = data[pack_type]
		if pack_value not in grouped_versions:
			grouped_versions[pack_value] = [version]
		else:
			grouped_versions[pack_value].append(version)
	result = []
	for pack_value, versions in grouped_versions.items():
		if len(versions) > 1:
			result.append(f"`{pack_value}` \u2500 `{versions[-1]} – {versions[0]}`")
		else:
			result.append(f"`{pack_value}` \u2500 `{versions[0]}`")
	return '\n'.join(result)
