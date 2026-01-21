import discord
from discord import app_commands
from discord.ext import commands

from utils import handle_errors, Emojis, check_author_from_cache


class DeleteBotMessage(commands.Cog):
	def __init__(self, bot: commands.Bot):
		super().__init__()
		self.bot = bot
		self.ctx_menu = app_commands.ContextMenu(
			name = "Удалить сообщение",
			callback = self.delete_bot_message,
		)
		bot.tree.add_command(self.ctx_menu)
	
	async def delete_bot_message(self, ctx: discord.Interaction, msg: discord.Message):
		if (
			(msg.author.id == self.bot.user.id and (
					(msg.interaction_metadata and msg.interaction_metadata.user.id == ctx.user.id) or
					(msg.reference and (await ctx.channel.fetch_message(msg.reference.message_id)).author.id == ctx.user.id)
				)
			) or
			(check_author_from_cache(ctx.user.id, msg.id))
		):
			await msg.delete()
			await ctx.response.send_message(f"{Emojis.check} Сообщение удалено", ephemeral=True)
		else:
			await handle_errors(ctx, Exception("not author"), [
				{
					"contains": "not author",
					"msg": "Вы не являетесь отправителем этого сообщения"
				}
			])

