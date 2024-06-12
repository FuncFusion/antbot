from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import Emojis


class SayCommand(commands.Cog):
	@commands.hybrid_command(aliases=["s", "сказать", "молвить", "сей", "сэй", "ыфн", "ы"],
		description="Отправляет сообщение от имени бота")
	@app_commands.describe(text="Текст сообщения, которое отправит бот")
	@app_commands.default_permissions(manage_messages=True)

	async def say(self, ctx, *, text: str):
		temp = await ctx.send("_ _", ephemeral=True)
		await ctx.channel.send(text)
		await temp.delete()
		await ctx.message.delete()

	@say.error
	async def say_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Введите текст который хотите сказать от моего имени"
			}
		])
