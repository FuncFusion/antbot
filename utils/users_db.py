from settings import DMS_LOGS_GUILD_ID, MONGO_URI

from pymongo.mongo_client import MongoClient

users_collection = MongoClient(MONGO_URI).antbot.users


class DB:
	class DMs:
		async def get_channel(user_id, bot):
			user_doc = users_collection.find_one({"_id": user_id})
			if not user_doc:
				await DB.add_user(user_id, bot)
				user_doc = users_collection.find_one({"_id": user_id})
			return await bot.fetch_channel(user_doc["dms_channel_id"])

	async def add_user(id, bot):
		id = int(id)
		# Check if user already exists in the database
		if users_collection.find_one({"_id": id}):
			return

		# Creating dms channel
		user = await bot.fetch_user(id)
		dms_log_guild = await bot.fetch_guild(DMS_LOGS_GUILD_ID)
		dms_log_channel = await dms_log_guild.create_text_channel(user.name, topic=str(id))

		# Adding user into db
		user_doc = {
			"_id": id,
			"dms_channel_id": dms_log_channel.id,
			"disapproved_ga": 0,
			"last_disapproved_ga": 0
		}
		users_collection.insert_one(user_doc)