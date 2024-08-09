import discord
from discord.ext import commands

from settings import HELP_FORUM_ID, CREATIONS_FORUM_ID

from utils.msg_utils import Emojis
from utils.shortcuts import no_ping
from utils.validator import validate

valid_pin = {
	"pin": ["пин", "закреп", "закрепи", "закрепить", ":pushpin:", "pushpin", "📌", "📍", "<:pushpin:1270666437496799254>"]
}


class Pin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_raw_reaction_add")
	async def react_to_pin(self, reaction):
		chnl = self.bot.get_channel(reaction.channel_id)
		if isinstance(chnl, discord.Thread) and chnl.parent_id in [HELP_FORUM_ID, CREATIONS_FORUM_ID] \
			and reaction.emoji.name == "📌":
			msg = await chnl.fetch_message(reaction.message_id)
			if reaction.member.id == chnl.owner_id or chnl.permissions_for(reaction.member).manage_messages:
				await msg.pin()
			else:
				pass
	
	@commands.Cog.listener("on_message")
	async def message_pin(self, msg):
		if isinstance(msg.channel, discord.Thread) and msg.channel.parent_id in (HELP_FORUM_ID, CREATIONS_FORUM_ID) \
		and (msg.author == msg.channel.owner or msg.author.guild_permissions.manage_messages):
			if validate(msg.content, valid_pin):
				try:
					replied_msg = await msg.channel.fetch_message(msg.reference.message_id)
					if replied_msg.pinned:
						await replied_msg.unpin()
					else:
						await replied_msg.pin()
					await msg.delete()
				except:
					await msg.reply(f"{Emojis.exclamation_mark} Ответьте на сообщение которе хотите закрепить/открепить", 
						allowed_mentions=no_ping, delete_after=5)

