import requests
from asyncio import sleep


async def snapshot_scraper(snapshot_channel):
	last_known_version = ""
	async def check_for_update():
		response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
		data = response.json()
		latest_version = data["versions"][0]["id"].replace(".", "-").replace("pre", "pre-release-")
		if latest_version != last_known_version:
			await snapshot_channel.send(f"<@&1245322215428329503>\nhttps://www.minecraft.net\
				/en-us/article/minecraft-{'snapshot-' if not 'pre' in latest_version else ''}\
				{latest_version}".replace("\t", ""))
		else:
			await sleep(900)
			await check_for_update()
	await check_for_update()
	
