import discord
from discord.ext import commands
from discord import app_commands

async def fake_send(user, channel, content, attachments=[], embeds=[]):
	files = []
	if attachments != []:
		for attachment in attachments:
			files.append(await attachment.to_file())
	user_copy_webhook = await channel.create_webhook(name=".")
	if attachments == [] and embeds == []:
		await user_copy_webhook.send(content=content, avatar_url=user.avatar.url, username=user.display_name)
	else:
		await user_copy_webhook.send(content=content, avatar_url=user.avatar.url, username=user.display_name, files=files, embeds=embeds)
	await user_copy_webhook.delete()