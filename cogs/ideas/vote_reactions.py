import discord
from discord.ext import commands
from discord import app_commands

from asyncio import sleep
from settings import IDEAS_CHANNEL_ID
from utils.msg_utils import Emojis

class IdeaVoteReactions(commands.Cog):

	@commands.Cog.listener("on_thread_create")
	async def vote_reactions(self, trd):
		await sleep(0.5)
		if trd.parent_id == IDEAS_CHANNEL_ID:
			await trd.starter_message.add_reaction(Emojis.antvote)
			await trd.starter_message.add_reaction(Emojis.downtvote)
			await trd.starter_message.pin()