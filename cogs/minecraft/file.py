import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING

from requests import get
from typing import List
from io import BytesIO
from pymongo import MongoClient

from settings import MONGO_URI
from utils.tree_gen import generate_tree
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.misc
files = {}
for tree_name in ("data", "assets"):
	tree = get(f"https://api.github.com/repos/misode/mcmeta/git/trees/{tree_name}?recursive=1").json().get("tree", [])
	files.update({"/".join(item["path"].split("/")[-2:]): item["path"] for item in tree if item["type"] == "blob"})
files.pop(".gitattributes")


class FileCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["f", "asset", "mcasset", "файл", "ашду", "ассет", "эссет", "мсассет", "мсэссэт","фыыуе","ьсфыыуе"], 
		description="Скидывает файл с ванильного датапака/ресурспака.",
		usage="`/file <путь/название интересующего файл>`",
		help="Слэш команда имеет автокомплит для файлов, что делает их поиск легче.\n### Пример:\n`/file colormap/grass`")
	@app_commands.describe(path="Путь/название интересующего файла")

	async def file(self, ctx, path: str):
		is_image = False
		all_results = [value for key, value in files.items() if path in value]
		path = all_results[0]
		#
		path_tree = ""
		for idx, part in enumerate(path.split("/")):
			path_tree += f"{' '*idx}{part}\n"
		path_tree = generate_tree(path_tree)
		#
		embed = discord.Embed(description=f"## <{path_tree.split("<")[-1].split(">")[0]}> {path.split('/')[-1]}\n{path_tree}",
			color=no_color)
		file = discord.File(BytesIO(get(f"https://raw.githubusercontent.com/misode/mcmeta/{path.split('/')[0]}/{path}").content), 
			filename=path.split("/")[-1])
		#
		if path.endswith("png"):
			embed.set_image(url=f"attachment://{file.filename}")
			is_image = True
		await ctx.reply(embed=embed, file=file if is_image else MISSING, allowed_mentions=no_ping)
		if not is_image:
			await ctx.channel.send(file=file)
	
	@file.error
	async def file_error(self, ctx, error):
		await handle_errors(ctx, error, [
		{
			"exception": commands.MissingRequiredArgument,
			"msg": "Не указан путь/название файла"
		},
		{
			"contains": "IndexError",
			"msg": "Файл по данному запросу не найден. Попробуйте воспользоватся **слэш** "
				"командой </file:1274682569715355688> для более удобного поиска"
		}
		])
	
	@file.autocomplete(name="path")
	async def file_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return [app_commands.Choice(name=key, value=value[-100:]) for key, value in files.items() if curr in value][:25]
