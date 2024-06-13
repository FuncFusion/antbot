from settings import MONGO_URI

import requests
from asyncio import sleep
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

db = MongoClient(MONGO_URI).antbot.misc


async def snapshot_scraper(snapshot_channel):
	async def check_for_update():
		last_known_version = db.find_one({"_id": "latest_known_snapshot"})["_"]
		response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
		data = response.json()
		latest_version_id = data["versions"][0]["id"]
		latest_version = latest_version_id.replace(".", "-").replace("pre", "pre-release-")\
		.replace("rc", "release-candidate-")
		if latest_version_id != last_known_version:
			db.update_one({"_id": "latest_known_snapshot"}, {"$set": {"_": latest_version_id}})
			await snapshot_channel.send(f"<@&1245322215428329503>\nhttps://www.minecraft.net\
				/en-us/article/minecraft-{'snapshot-' if latest_version == latest_version_id else ''}\
				{'java-edition-' if data['versions'][0]['type'] == 'release' else ''}{latest_version}".replace("\t", ""))
		else:
			await sleep(900)
			await check_for_update()
	await check_for_update()
	
