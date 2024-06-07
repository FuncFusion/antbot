import discord
from discord.ext import commands
from discord import app_commands

from utils.msg_utils import Emojis
from utils.shortcuts import no_ping

async def pfp_ratelimit_msg(self, ctx, error):
	await ctx.reply(f"{Emojis.mojo} Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже", allowed_mentions=no_ping)


class StatusCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
		description="Отключает бота.")
	@app_commands.default_permissions(manage_guild=True)
	async def shutdown(self, ctx):
		with open("assets/pfps/offline.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		await ctx.reply("Отключаюсь... 😴", allowed_mentions=no_ping)
		await self.bot.close()
	shutdown.error(pfp_ratelimit_msg)

	@commands.hybrid_command(aliases=["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
		description="Меняет статус бота на \"В сети\".")
	@app_commands.default_permissions(manage_guild=True)
	async def online(self, ctx):
		with open("assets/pfps/online.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		if self.bot.get_guild(1142344574501658694).me.status != discord.Status.online:
			await ctx.reply("Теперь мой статус - `В сети`.", allowed_mentions=no_ping)
			await self.bot.change_presence(status=discord.Status.online)
		else:
			await ctx.reply("У меня и так статус `В сети`.")
	online.error(pfp_ratelimit_msg)

	@commands.hybrid_command(aliases=["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
		description="Меняет статус бота на \"Отошёл\".")
	@app_commands.default_permissions(manage_guild=True)
	async def idle(self, ctx):
		with open("assets/pfps/idle.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		if self.bot.get_guild(1142344574501658694).me.status != discord.Status.idle:
			await ctx.reply("Теперь мой статус - `Отошёл`.", allowed_mentions=no_ping)
			await self.bot.change_presence(status=discord.Status.idle)
		else:
			await ctx.reply("У меня и так статус `Отошёл`.")
	idle.error(pfp_ratelimit_msg)

	@commands.hybrid_command(aliases=["dnd", "do-not-disturb", "небеспокоить", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
		description="Меняет статус бота на \"Не беспокоить\".")
	@app_commands.default_permissions(manage_guild=True)
	async def donotdisturb(self, ctx):
		with open("assets/pfps/dnd.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		if self.bot.get_guild(1142344574501658694).me.status != discord.Status.do_not_disturb:
			await ctx.reply("Теперь мой статус - `Не беспокоить`.", allowed_mentions=no_ping)
			await self.bot.change_presence(status=discord.Status.do_not_disturb)
		else:
			await ctx.reply("У меня и так статус `Не беспокоить`.")
	donotdisturb.error(pfp_ratelimit_msg)

	@commands.hybrid_command(aliases=["invis", "inv", "невидимка", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"],
		description="Меняет статус бота на \"Невидимка\".")
	@app_commands.default_permissions(manage_guild=True)
	async def invisible(self, ctx):
		with open("assets/pfps/offline.png", "rb") as file:
			await self.bot.user.edit(avatar=file.read())
		if self.bot.get_guild(1142344574501658694).me.status != discord.Status.invisible:
			await ctx.reply("Теперь мой статус - `Невидимка`.", allowed_mentions=no_ping)
			await self.bot.change_presence(status=discord.Status.invisible)
		else:
			await ctx.reply("У меня и так статус `Невидимка`.")
	invisible.error(pfp_ratelimit_msg)
