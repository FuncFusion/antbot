import discord
from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import get_msg_by_id_arg, Emojis


class EditCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["изменить", "эдит", "увше"],
		description="Изменяет заданное сообщение.")
	@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")
	@app_commands.default_permissions(manage_messages=True)

	async def edit(self, ctx, message:str, *, text:str):
		if ctx.message.reference == None:
			msg = await get_msg_by_id_arg(self, ctx, self.bot, message)
			await discord.Message.edit(self=msg,content=text)
		else:
			msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			await discord.Message.edit(self=msg, content=message+" "+text)

	@edit.error
	async def edit_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Не хватает аргументов"
			},
			{
				"contains": "403 Forbidden",
				"msg": f"{Emojis.exclamation_mark} Не могу изменять чужие сообщения"
			},
			{
				"contains": "'NotFound'",
				"msg": f"{Emojis.exclamation_mark} Не нашёл сообщения с таким айди"
			},
			{
				"contains": "'ValueError'",
				"msg": f"{Emojis.exclamation_mark} Введён неверный айди"
			}
		])