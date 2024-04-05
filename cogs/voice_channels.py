import discord
from discord.ext import commands
from discord import app_commands

from settings import VCS_CATEGORY_ID, CREATE_VC_CHANNEL_ID
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color

class CustomVoiceChannels(commands.Cog, name="Голосовые каналы"):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_voice_state_update")
	async def create_new_vc(self, member, before, after):
		if after.channel != None and after.channel.id == CREATE_VC_CHANNEL_ID:
			vcs_category = self.bot.get_channel(VCS_CATEGORY_ID)
			memeber_s_vc = await vcs_category.create_voice_channel(name=member.display_name)
			await member.move_to(memeber_s_vc)
			await memeber_s_vc.set_permissions(member, manage_channels=True, mute_members=True, 
				deafen_members=True, move_members=True)
	
	@commands.Cog.listener("on_voice_state_update")
	async def delete_vc(self, member, before, after):
		if before.channel not in [after.channel, None] and before.channel.id != CREATE_VC_CHANNEL_ID and \
		before.channel.category_id == VCS_CATEGORY_ID and len(before.channel.members) == 0:
			await before.channel.delete()