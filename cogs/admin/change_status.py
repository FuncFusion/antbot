import discord
from discord.ext import commands
from discord import app_commands

from typing import Literal

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping
from utils.validator import validate, closest_match


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


	@commands.has_permissions(manage_guild=True)
	@commands.hybrid_command(name="status",
		aliases=["ыефегы", "статус"],
		description="**Админская команда.** Меняет статус и аватарку бота.",
		usage="`/status <Онлайн|Отошёл|Не беспокоить|Оффлайн>`",
		help="Вместе с изменением статуса антбот меняет аватарку, меняя цвет ядра в его груди. Кроме предложенных аргументов можно также использовать алиасы этих статусов, например, `afk`, `dnd`, `невидимка`, `всети`.\n### Пример:\n`/status Отошёл`")
	@app_commands.default_permissions(manage_guild=True)
	async def change_status(self, ctx, *, status):
		valid_statuses = {
			"online": ["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
			"idle": ["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
			"dnd": ["do-not-disturb", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
			"offline": ["Оффлайн", "invis", "невидимка", "inv", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"]
		}
		status = closest_match(status, valid_statuses, 15)
		can_change_avatar = ""
		if status is None:
			raise Exception("Неверно введено название статуса")
		try:
			with open(f"assets/pfps/{status}.png", "rb") as file:
				await self.bot.user.edit(avatar=file.read())
		except:
			can_change_avatar = "Но аватарку так быстро менять не могу."
		await self.bot.change_presence(status=discord.Status(value=status))
		await ctx.reply(f"{Emojis.check} Теперь мой статус — `{valid_statuses[status][1]}`. {can_change_avatar}", allowed_mentions=no_ping)
	@change_status.error
	async def status_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingPermissions,
				"msg": f"Недостаточно прав"
			},
			{
				"contains": "Неверно введено название статуса",
				"msg": f"Неверно введено название статуса"
			}
		])
