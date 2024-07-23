from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import Emojis


class SayCommand(commands.Cog):
	@commands.has_permissions(ban_members=True)
	@commands.hybrid_command(aliases=["tell", "сказать", "молвить", "сей", "сэй", "ыфн"],
		description="Отправляет сообщение от имени бота")
	@app_commands.describe(text="Текст сообщения, которое отправит бот")

	async def say(self, ctx, *, text: str):
		await ctx.channel.send(text)
		if ctx.interaction:
			await ctx.send("_ _", ephemeral=True, delete_after=0)
		else:
			await ctx.message.delete()

	@say.error
	async def say_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Введите текст который хотите сказать от моего имени"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
