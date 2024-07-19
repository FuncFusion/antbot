import discord
from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.msg_utils import get_msg_by_id_arg, Emojis


class EditCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.has_permissions(ban_members=True)
	@commands.hybrid_command(aliases=["изменить", "эдит", "увше"],
		description="Изменяет заданное сообщение.")
	@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")

	async def edit(self, ctx, message:str, *, text:str=""):
		mentions = discord.AllowedMentions.none()
		if ctx.message.reference == None:
			msg = await get_msg_by_id_arg(self, ctx, self.bot, message)
			if msg.mentions != []: mentions = discord.AllowedMentions.all()
			await discord.Message.edit(self=msg, content=text[:2000], allowed_mentions=mentions)
		else:
			msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			if msg.mentions != []: mentions = discord.AllowedMentions.all()
			content = message+" "+text
			await discord.Message.edit(self=msg, content=content[:2000], allowed_mentions=mentions)
		if ctx.interaction:
			await ctx.send(f"{Emojis.check} Сообщение отредактировано", ephemeral=True)

	@edit.error
	async def edit_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов"
			},
			{
				"contains": "403 Forbidden",
				"msg": "Не могу изменять чужие сообщения"
			},
			{
				"contains": "'NotFound'",
				"msg": "Не нашёл сообщения с таким айди"
			},
			{
				"contains": "'ValueError'",
				"msg": "Введён неверный айди"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": "Недостаточно прав"
			}
		])
