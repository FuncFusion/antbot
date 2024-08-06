import discord
from discord.ext import commands
from discord import app_commands

from typing import Literal

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping
from utils.validator import validate


class StatusCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	# @commands.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
	# 	description="Отключает бота.")
	# @commands.has_permissions(manage_guild=True)
	# async def shutdown(self, ctx):
	# 	with open("assets/pfps/offline.png", "rb") as file:
	# 		await self.bot.user.edit(avatar=file.read())
	# 	await ctx.reply("Отключаюсь... 😴", allowed_mentions=no_ping)
	# 	await self.bot.close()
	# @shutdown.error
	# async def off_error(self, ctx, error):
	# 	await handle_errors(ctx, error, [
	# 		{
	# 			"contains": "HTTPException",
	# 			"msg": f" {Emojis.mojo} Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже"
	# 		},
	# 		{
	# 			"exception": commands.MissingPermissions,
	# 			"msg": "Недостаточно прав"
	# 		}
	# 	])


	@commands.hybrid_command(name="status", aliases=["ыефегы", "статус"],
		description="Меняет статус бота")
	@commands.has_permissions(manage_guild=True)
	async def change_status(self, ctx, status: Literal["Онлайн", "Отошёл", "Не беспокоить", "Оффлайн"]):
		valid_statuses = {
			"online": ["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
			"idle": ["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
			"dnd": ["dnd", "не беспокоить", "do-not-disturb", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
			"offline": ["invis", "невидимка", "inv", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"]
		}
		status = validate(status, valid_statuses)
		with open(f"assets/pfps/{status}.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		await self.bot.change_presence(status=discord.Status(value=status))
		await ctx.reply(f"{Emojis.check} Теперь мой статус - `{valid_statuses[status][1]}`.", allowed_mentions=no_ping)
	@change_status.error
	async def status_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "HTTPException",
				"msg": f" {Emojis.mojo} Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже"
			},
			{
				"exception": commands.MissingPermissions,
				"msg": f"Недостаточно прав"
			},
			{
				"contains": "Could not convert",
				"msg": f"Неверно введено название статуса"
			}
		])
