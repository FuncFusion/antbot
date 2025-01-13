import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import MISSING

from Levenshtein import distance
from aiohttp import ClientSession
from typing import List
from io import BytesIO
from pymongo import MongoClient

from settings import MONGO_URI, GITHUB_HEADERS, LOGS_CHANNEL_ID
from utils.tree_gen import generate_tree
from utils.general import handle_errors
from utils.shortcuts import no_color, no_ping

db = MongoClient(MONGO_URI).antbot.minecraft_data
versions_pathes = MongoClient(MONGO_URI).antbot.versions_pathes
files = []
latest_version = ""
logs_channel = None


class FileCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.update_files_list.start()
	
	async def get_files_list(self, branches=("data", "assets")):
		async with ClientSession(headers=GITHUB_HEADERS) as session:
			current_files = []
			for branch in branches:
				async with session.get(f"https://api.github.com/repos/misode/mcmeta/git/trees/{branch}?recursive=1") as response:
					if response.status == 200:
						tree = await response.json()
						tree = tree.get("tree", [])
						current_files += [
							item["path"] 
							for item in tree if item["type"] == "blob"
						]
					else:
						raise Exception(f"Response error")
			try:
				current_files.remove(".gitattributes")
			except:pass
		return current_files

	@tasks.loop(minutes=6)
	async def update_files_list(self):
		global latest_version, files
		if (newer_version:=db.find_one({"_id": "latest_known_snapshot"})["_"]) != latest_version:
			if (latest_files := versions_pathes.find_one({"_id": newer_version.replace('.', '_')})):
				files = latest_files["_"]
			else:
				try:
					files = await self.get_files_list()
					await self.update_versions_hashes(newer_version)
					latest_version = newer_version
					versions_pathes.insert_one({"_id": latest_version.replace('.', '_'), "_": files})
				except:pass

	async def update_versions_hashes(self, newer_version=None):
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
								version = commit["commit"]["message"].split(" ")[-1].replace(".", "_")
								versions_hashes[branch][version] = commit["sha"]
						else:
							print(f"Failed to fetch commits. Status code: {response.status}")
							break
				page += 1
		if newer_version and not (newer_version.replace(".", "_") in versions_hashes["data"]):
			raise Exception("Mcmeta not updated")
		db.update_one({"_id": "versions_hashes"}, {"$set": {"_": versions_hashes}}, upsert=True)


	@commands.hybrid_command(
		aliases=["f", "asset", "mcasset", "файл", "ашду", "ассет", "эссет", "мсассет", "мсэссэт","фыыуе","ьсфыыуе"], 
		description="Скидывает файл с ванильного датапака/ресурспака.",
		usage="`/file <путь/название интересующего файл>`",
		help="Структура файлов обновляется в течении 6 минут сразу после выхода новой версии/снапшота. Слэш команда имеет автокомплит для файлов, что делает их поиск легче.\n### Пример:\n`/file colormap/grass`") 
	@app_commands.describe(path="Путь/название интересующего файла")

	async def file(self, ctx, path: str, version: str="latest"):
		def search_files(query, files):
			matches = []
			for file in files:
				if query in file:
					matches.append(file)
				else:
					match_count = 0
					query_items_backwards = query.split("/")[::-1]
					query_size = len(query_items_backwards)
					for i in query_items_backwards:
						for j in file.split("/")[::-1]:
							if distance(i, j) <= len(i)/3:
								match_count += 1
								break
						if match_count >= query_size:
							matches.append(file)
							break
			return matches
		is_image = False
		if version == "latest":
			current_files = files
		else:
			version_for_mongo = version.replace(".", "_")
			versions_hashes = db.find_one({"_id": "versions_hashes"})["_"]
			if version_for_mongo not in versions_hashes["data"]:
				raise Exception("Wrong version")
			if (files_for_version:=versions_pathes.find_one({"_id": version_for_mongo})) != None:
				current_files = files_for_version["_"]
			else:
				current_files = await self.get_files_list((
					versions_hashes["data"][version_for_mongo],
					versions_hashes["assets"][version_for_mongo]
				))
				versions_pathes.insert_one({"_id": version_for_mongo, "_": current_files})
		all_results = search_files(path, current_files)
		path = all_results[0]
		#
		path_tree = ""
		for idx, part in enumerate(path.split("/")):
			path_tree += f"{' '*idx}{part}\n"
		path_tree = generate_tree(path_tree)
		#
		branch = path.split("/")[0]
		if version != "latest":
			branch = versions_hashes[branch][version_for_mongo]
		async with ClientSession(headers=GITHUB_HEADERS) as session:
			async with session.get(f"https://raw.githubusercontent.com/misode/mcmeta/{branch}/{path}") as response:
				if response.status != 200:
					raise Exception(f"Response error {response.status}")
				file = discord.File(BytesIO(await response.read()), filename=path.split("/")[-1])
		#
		embed = discord.Embed(description=f"## <{path_tree.split("<")[-1].replace("`","")} ({version})\n{path_tree}",
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
				"командой </file:1276634233221156957> для более удобного поиска"
		}
		])
	
	@file.autocomplete(name="path")
	async def file_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		if (version:=ctx.namespace.version) != None:
			version = version.replace('.', '_')
			if (files_for_version:=versions_pathes.find_one({"_id": version})):
				current_files = files_for_version["_"]
			else:
				versions_hashes = db.find_one({"_id": "versions_hashes"})["_"]
				if version not in versions_hashes["data"]:
					current_files = files
				else:
					current_files = await self.get_files_list((
						versions_hashes["data"][version],
						versions_hashes["assets"][version]
					))
					versions_pathes.insert_one({"_id": version, "_": current_files})
		else:
			current_files = files
		return [
			app_commands.Choice(name=file[-100:], value=file[-100:]) 
			for file in current_files if curr in file
		][:25]
