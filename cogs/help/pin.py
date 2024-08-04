import discord
from discord.ext import commands

from settings import HELP_FORUM_ID, CREATIONS_FORUM_ID

from utils.msg_utils import Emojis


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
