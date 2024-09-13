import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import MISSING

from aiohttp import ClientSession
from typing import List
from io import BytesIO
from pymongo import MongoClient

from settings import MONGO_URI, GITHUB_HEADERS
from utils.tree_gen import generate_tree
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.minecraft_data
files = {}
latest_version = ""


class FileCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.update_files_list.start()
	
	async def get_files_list(self, branches=("data", "assets")):
		async with ClientSession(headers=GITHUB_HEADERS) as session:
			for branch in branches:
				async with session.get(f"https://api.github.com/repos/misode/mcmeta/git/trees/{branch}?recursive=1") as response:
					tree = await response.json()
					tree = tree.get("tree", [])
					files.update({
						"/".join(item["path"].split("/")[-2:]): item["path"] 
						for item in tree if item["type"] == "blob"
					})
			try:
				files.pop(".gitattributes")
			except:pass
		return files

	@tasks.loop(minutes=6)
	async def update_files_list(self):
		global latest_version, files
		if (newer_version:=db.find_one({"_id": "latest_known_snapshot"})["_"]) != latest_version:
			latest_version = newer_version
			files = await self.get_files_list()
			db.update_one({"_id": "versions_pathes"}, {"$set": {latest_version: files}}, upsert=True)
			await self.update_versions_hashes()

	async def update_versions_hashes(self):
		versions_hashes = db.find_one({"_id": "versions_hashes"})
		if versions_hashes:
			versions_hashes = versions_hashes["_"]
		else:
			versions_hashes = {"assets": {}, "data": {}}
		for branch in ("assets", "data"):
			page = 1
			while True:
				url = f"https://api.github.com/repos/misode/mcmeta/commits?sha={branch}&per_page=100&page={page}"
				async with ClientSession(headers=GITHUB_HEADERS) as session:
					async with session.get(url) as response:
						if response.status == 200:
							data = await response.json()
							if not data:
								break
							for commit in data:
								version = commit["commit"]["message"].split(" ")[-1]
								versions_hashes[branch][version] = commit["sha"]
						else:
							print(f"Failed to fetch commits. Status code: {response.status}")
							break
				page += 1
		db.update_one({"_id": "versions_hashes"}, {"$set": {"_": versions_hashes}}, upsert=True)

	@commands.hybrid_command(aliases=["f", "asset", "mcasset", "файл", "ашду", "ассет", "эссет", "мсассет", "мсэссэт","фыыуе","ьсфыыуе"], 
		description="Скидывает файл с ванильного датапака/ресурспака.",
		usage="`/file <путь/название интересующего файл>`",
		help="Структура файлов обновляется в течении 6 минут сразу после выхода новой версии/снапшота. Слэш команда имеет автокомплит для файлов, что делает их поиск легче.\n### Пример:\n`/file colormap/grass`") 
	@app_commands.describe(path="Путь/название интересующего файла")

	async def file(self, ctx, path: str, version: str="latest"):
		is_image = False
		if version == "latest":
			current_files = files
		else:
			versions_hashes = db.find_one({"_id": "versions_hashes"})["_"]
			if version not in versions_hashes["data"]:
				raise Exception("Wrong version")
			#
			versions_pathes = db.find_one({"_id": "versions_pathes"})["_"]
			if version in versions_pathes:
				current_files = versions_pathes[version]
			else:
				current_files = await self.get_files_list((
					versions_hashes["data"][version],
					versions_hashes["assets"][version]
				))
				db.update_one({"_id": "versions_pathes"}, {"$set": {f"_.{version.replace('.', '\\.')}": current_files}})
		all_results = [value for key, value in current_files.items() if path in value]
		path = all_results[0]
		#
		path_tree = ""
		for idx, part in enumerate(path.split("/")):
			path_tree += f"{' '*idx}{part}\n"
		path_tree = generate_tree(path_tree)
		#
		branch = path.split("/")[0]
		if version != "latest":
			branch = versions_hashes[branch][version]
		async with ClientSession(headers=GITHUB_HEADERS) as session:
			async with session.get(f"https://raw.githubusercontent.com/misode/mcmeta/{branch}/{path}") as response:
				if response.status != 200:
					raise Exception(f"Response error {response.status}")
				file = discord.File(BytesIO(await response.read()), filename=path.split("/")[-1])
		#
		embed = discord.Embed(description=f"## <{path_tree.split("<")[-1].split(">")[0]}> {path.split('/')[-1]} ({version})\n{path_tree}",
			color=no_color)
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
			"contains": "Wrong version",
			"msg": "Указанная версия не найдена"
		},
		{
			"contains": "Response error",
			"msg": "Файл не найден/Рейт лимит (попробуйте позже)"
		},
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
		if (version:=ctx.namespace.version) != None:
			versions_pathes = db.find_one({"_id": "versions_pathes"})["_"]
			if version in versions_pathes:
				current_files = versions_pathes[version]
				print("gex")
			else:
				versions_hashes = db.find_one({"_id": "versions_hashes"})["_"]
				current_files = await self.get_files_list((
					versions_hashes["data"][version],
					versions_hashes["assets"][version]
				))
				db.update_one({"_id": "versions_pathes"}, {"$set": {f"_.{version.replace('.', '\\.')}": current_files}})
		else:
			current_files = files.copy()
		return [app_commands.Choice(name=key, value=value[-100:]) for key, value in current_files.items() if curr in value][:25]
