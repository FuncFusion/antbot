import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

async def fake_send(user, channel, content, attachments=MISSING, embeds=MISSING):
	files = MISSING
	thread = MISSING
	if attachments != MISSING:
		files = []
		for attachment in attachments:
			files.append(await attachment.to_file())
	if isinstance(channel, discord.Thread):
		thread = channel
		channel = channel.parent
	user_copy_webhook = await channel.create_webhook(name=".")
	if isinstance(content, list):
		for text in content:
			if text == content[-1]:
				await user_copy_webhook.send(content=text, avatar_url=user.avatar.url, username=user.display_name, 
				files=files, thread=thread)
			else:
				await user_copy_webhook.send(content=text, avatar_url=user.avatar.url, username=user.display_name, thread=thread)	
	else:
		await user_copy_webhook.send(content=content, avatar_url=user.avatar.url, username=user.display_name, 
		thread=thread, files=files)
	await user_copy_webhook.delete()
