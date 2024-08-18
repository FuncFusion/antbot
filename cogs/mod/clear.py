import discord
from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


class ClearCommand(commands.Cog):

	@commands.has_permissions(manage_messages=True)
	@commands.hybrid_command(
		aliases=["сдуфк", "клир", "очистить"],
		description="**Модераторская команда.** Очищает сообщения в указанном канале.",
		usage="`/clear <количество сообщений> [канал (по дефолту текущий)]`",
		help="### Пример:\n`/clear 16`")
	@app_commands.default_permissions(manage_messages=True)
	@app_commands.describe(count="Количество сообщений, которое будет удалено", channel="Канал, в котором будут удалены сообщения")

	async def clear(self, ctx, count: int, channel: discord.TextChannel=None):
		channel = channel if channel != None else ctx.channel
		if count < 1:
			raise Exception("count")
		if ctx.interaction:
			await ctx.message.delete()
		await channel.purge(limit=count)
		await ctx.send(f"{Emojis.check} Удалено {count} сообщения", delete_after=8, ephemeral=True)

	@clear.error
	async def clear_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "count",
				"msg": "Количество сообщений должно быть больше или равно 1"
			},
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите количество сообщений которое будет удалено"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
