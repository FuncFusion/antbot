from discord.ext import commands, tasks

from settings import MONGO_URI, SNAPSHOT_PING_ROLE, SNAPSHOTS_CHANNEL_ID

import requests
from pymongo.mongo_client import MongoClient

db = MongoClient(MONGO_URI).antbot.misc

class SnapshotScraper(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.check_for_update.start()

	@tasks.loop(minutes=30)
	async def check_for_update(self):
		snapshot_channel = await self.bot.fetch_channel(SNAPSHOTS_CHANNEL_ID)
		last_known_version = db.find_one({"_id": "latest_known_snapshot"})["_"]
		response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
		data = response.json()
		latest_version_id = data["versions"][0]["id"]
		latest_version = latest_version_id.replace(".", "-").replace("pre", "pre-release-")\
		.replace("rc", "release-candidate-")
		if latest_version_id != last_known_version:
			db.update_one({"_id": "latest_known_snapshot"}, {"$set": {"_": latest_version_id}})
			snapshot_msg = await snapshot_channel.send(f"<@&{SNAPSHOT_PING_ROLE}>\nhttps://www.minecraft.net"
				f"/en-us/article/minecraft-{'snapshot-' if latest_version == latest_version_id else ''}"
				f"{'java-edition-' if data['versions'][0]['type'] == 'release' else ''}{latest_version}")
			await snapshot_msg.pin()
	
