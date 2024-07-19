from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import Emojis


class DebugCommand(commands.Cog):
	@commands.has_permissions(ban_members=True)
	@commands.command(aliases=["d"])

	async def debug(self, ctx, *, text: str):
		try:
			evaled = str(eval(text))
		except Exception as e:
			evaled = str(e)
		await ctx.channel.send(evaled)

	@debug.error
	async def say_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"Введите текст который хотите сказать от моего имени"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": f"Недостаточно прав"
			}
		])
