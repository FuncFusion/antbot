import discord
from discord.ext import commands
from discord import app_commands

from settings import DMS_LOGS_GUILD_ID

from json import load, dump

class DB:
	class DMs:
		async def get_channel(user_id, bot):
			user_id = str(user_id)
			db = DB.get()
			if user_id not in db:
				await DB.add_user(user_id, bot)
			db = DB.get()
			return bot.get_channel(db[user_id]["dms_channel_id"])
	
	def get():
		with open("users.json", "r", encoding="utf-8") as db_f:
			return load(db_f)

	async def add_user(id, bot):
		id = str(id)
		db = DB.get()
		# Creating dms channel
		user = await bot.fetch_user(int(id))
		dms_log_guild = await bot.fetch_guild(DMS_LOGS_GUILD_ID)
		dms_log_channel = await dms_log_guild.create_text_channel(user.name)
		# Adding user intо db
		db[id] = {
			"economy": {
				"antoins": 0,
				"auto-workers": []
			},
			"dms_channel_id": dms_log_channel.id
		}
		with open("users.json", "w", encoding="utf-8") as db_f:
			dump(db, db_f, ensure_ascii=False, indent="\t")
