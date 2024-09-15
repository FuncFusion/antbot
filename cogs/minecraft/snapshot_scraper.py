from discord.ext import commands, tasks

from settings import MONGO_URI, SNAPSHOT_PING_ROLE, SNAPSHOTS_CHANNEL_ID
from utils.msg_utils import Emojis

from aiohttp import ClientSession
from asyncio import sleep
from pymongo.mongo_client import MongoClient

db = MongoClient(MONGO_URI).antbot.minecraft_data


class SnapshotScraper(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.check_for_update.start()
	
	@commands.Cog.listener(name="on_message")
	async def on_version_release(self, msg):
		if "Mojira" in msg.author.name and msg.author.bot and "has been released." in msg.content:
			latest_known_version = db.find_one({"_id": "latest_known_snapshot"})["_"]
			waiting_msg = await msg.reply(f"{Emojis.typing} Найс, жду ченжлог")
			#
			for i in range(6):
				self.check_for_update.cancel()
				await sleep(1)
				self.check_for_update.start()
				if db.find_one({"_id": "latest_known_snapshot"})["_"] != latest_known_version:
					break
				await sleep(60)
			await waiting_msg.delete()

	@tasks.loop(minutes=12)
	async def check_for_update(self):
		snapshot_channel = await self.bot.fetch_channel(SNAPSHOTS_CHANNEL_ID)
		last_known_version = db.find_one({"_id": "latest_known_snapshot"})["_"]
		async with ClientSession() as session:
			async with session.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", 
				headers={"User-Agent": "AntBot discord bot"}) as response:
				data = await response.json()
		latest_version_id = data["versions"][0]["id"]
		# Formatting name
		latest_version = latest_version_id\
			.replace(".", "-")\
			.replace("pre", "pre-release-")\
			.replace("rc", "release-candidate-")
		#
		if latest_version_id != last_known_version:
			db.update_one({"_id": "latest_known_snapshot"}, {"$set": {"_": latest_version_id}})
			snapshot_msg = await snapshot_channel.send(f"<@&{SNAPSHOT_PING_ROLE}>\nhttps://www.minecraft.net"
				f"/en-us/article/minecraft-{'snapshot-' if latest_version == latest_version_id else ''}"
				f"{'java-edition-' if data['versions'][0]['type'] == 'release' else ''}{latest_version}")
			await snapshot_msg.pin()
	
