import discord
from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


class ClearCommand(commands.Cog):

	@commands.has_permissions(manage_messages=True)
	@commands.hybrid_command(aliases=["сдуфк", "клир", "очистить"], description="Очищает сообщения")
	@app_commands.describe(count="Количество сообщений которое будет удалено", channel="Канал в котором будут удалены сообщения")

	async def clear(self, ctx, count: int, channel: discord.TextChannel=None):
		channel = channel if channel != None else ctx.channel
		await channel.purge(limit=count + (1 if channel == ctx.channel else 0))
		await ctx.send("Удалено 3 сообщения", delete_after=0)

	@clear.error
	async def clear_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Пожалуйста, укажите количество сообщений которое будет удалено"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": f"{Emojis.exclamation_mark} Недостаточно прав"
			}
		])
