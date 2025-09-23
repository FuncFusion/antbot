import discord
from discord.utils import MISSING, _MissingSentinel

from pymongo.mongo_client import MongoClient

from settings import MONGO_URI, DISCORD_API_SECRET
from utils.shortcuts import no_ping

db = MongoClient(MONGO_URI).antbot.webhook_channels


async def fake_send(user, 
	channel, 
	content=MISSING, 
	attachments=MISSING, 
	embeds=MISSING, 
	view=MISSING, 
	thread_name=MISSING, 
	allowed_mentions=no_ping
):
	files = MISSING
	thread = MISSING
	if not isinstance(attachments, _MissingSentinel):
		files = []
		for attachment in attachments:
			files.append(await attachment.to_file())
	if isinstance(channel, discord.Thread):
		thread = channel
		channel = channel.parent
	# The hook
	if (doc:=db.find_one({"_id": channel.id})):
		for wh in await channel.webhooks():
			if wh.id == doc["webhook_id"]:
				user_copy_webhook = wh
				break
	else:
		user_copy_webhook = await channel.create_webhook(name=".")
		db.insert_one({"_id": channel.id, "webhook_id": user_copy_webhook.id})
	#
	if isinstance(content, list):
		for text in content:
			if text == content[-1]:
				await user_copy_webhook.send(content=text, avatar_url=user.display_avatar.url, username=user.display_name, 
				files=files, thread=thread, allowed_mentions=allowed_mentions)
			else:
				await user_copy_webhook.send(content=text, avatar_url=user.display_avatar.url, username=user.display_name, thread=thread, allowed_mentions=allowed_mentions)	
	else:
		msg = await user_copy_webhook.send(content=content, avatar_url=user.display_avatar.url, username=user.display_name, 
		thread=thread, thread_name=thread_name, embeds=embeds, view=view, files=files, allowed_mentions=allowed_mentions, wait=True)
		return msg
