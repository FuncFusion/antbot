import discord
from discord.ext import commands
from discord import app_commands

from settings import VCS_CATEGORY_ID, CREATE_VC_CHANNEL_ID
from utils.general import handle_errors
from utils.msg_utils import Emojis

class CustomVoiceChannels(commands.Cog, name="Голосовые каналы"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(name="transfer-ownership", aliases=["передать-права", "to", "пп"], \
		description="Передать права на голосовой канал")
	@app_commands.describe(user="Пользователь")
	@app_commands.default_permissions(manage_channels=True)
	async def transfer_owner(self, ctx, user: discord.Member):	
		if ctx.channel.category_id == VCS_CATEGORY_ID and ctx.channel.permissions_for(ctx.author).manage_channels:
			await ctx.channel.set_permissions(ctx.author, manage_channels=None, mute_members=None, 
				deafen_members=None, move_members=None)
			await ctx.channel.set_permissions(user, manage_channels=True, mute_members=True, 
				deafen_members=True, move_members=True)
			await ctx.send(f"{Emojis.check} Права переданы {user.mention}", ephemeral=True)
	@transfer_owner.error
	async def to_error(self, ctx, error):
		await handle_errors(ctx, error, [])

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