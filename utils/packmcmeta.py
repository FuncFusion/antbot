from discord.ext import tasks

from settings import MONGO_URI, GITHUB_HEADERS
from aiohttp import ClientSession
from pymongo.mongo_client import MongoClient

db = MongoClient(MONGO_URI).antbot.minecraft_data

latest_version = ""

@tasks.loop(minutes=3)
async def update_mcmeta_info():
	global latest_version
	if (newer_version:=db.find_one({"_id": "latest_known_snapshot"})["_"]) != latest_version:
		async with ClientSession(headers=GITHUB_HEADERS) as session:
			async with session.get("https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json", 
				) as response:
				if response.status == 200:
					versions_original = await response.json(content_type=None)
					versions = {ver["id"]: {
						"type": ver["type"],
						"data_pack": ver["data_pack_version"],
						"resource_pack": ver["resource_pack_version"]} for ver in versions_original}
					versions["latest"] = {
						"type": versions_original[0]["type"],
						"data_pack": versions_original[0]["data_pack_version"],
						"resource_pack": versions_original[0]["resource_pack_version"],
						"id": versions_original[0]["id"]}
					db.update_one({"_id": "pack_format"}, {"$set": {"_": versions}}, upsert=True)
					latest_version = newer_version


def get_mcmeta_ver(pack="data_pack", requested_version="latest"):
	versions = db.find_one({"_id": "pack_format"})["_"]
	if requested_version == "latest":
		return versions["latest"][pack]
	elif requested_version == "all":
		return versions
	else:
		try:
			return versions[requested_version][pack]
		except:
			return None

