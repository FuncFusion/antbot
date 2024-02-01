import discord
from discord.ext import commands
from discord import app_commands
from utils.msg_utils import get_msg_by_id_arg
from utils.emojis import Emojis

from utils.shortcuts import no_ping, no_color

async def pfp_ratelimit_msg(ctx, error):
	await ctx.reply(f"{Emojis.mojo} Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже", allowed_mentions=no_ping)
	
class AdminCommands(commands.Cog):
	def __init__(self, bot):
		
		@bot.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
							description="Отключает бота.")
		@app_commands.default_permissions(manage_guild=True)
		async def shutdown(ctx):
			with open("assets/pfps/offline.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
			await ctx.reply("Отключаюсь... 😴", allowed_mentions=no_ping)
			await bot.close()
		shutdown.error(pfp_ratelimit_msg)

		@bot.hybrid_command(aliases=["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
							description="Меняет статус бота на \"В сети\".")
		@app_commands.default_permissions(manage_guild=True)
		async def online(ctx):
			with open("assets/pfps/online.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
			if bot.get_guild(1142344574501658694).me.status != discord.Status.online:
				await ctx.reply("Теперь мой статус - `В сети`.", allowed_mentions=no_ping)
				await bot.change_presence(status=discord.Status.online)
			else:
				await ctx.reply("У меня и так статус `В сети`.")
		online.error(pfp_ratelimit_msg)

		@bot.hybrid_command(aliases=["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
							description="Меняет статус бота на \"Отошёл\".")
		@app_commands.default_permissions(manage_guild=True)
		async def idle(ctx):
			with open("assets/pfps/idle.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
			if bot.get_guild(1142344574501658694).me.status != discord.Status.idle:
				await ctx.reply("Теперь мой статус - `Отошёл`.", allowed_mentions=no_ping)
				await bot.change_presence(status=discord.Status.idle)
			else:
				await ctx.reply("У меня и так статус `Отошёл`.")
		idle.error(pfp_ratelimit_msg)

		@bot.hybrid_command(aliases=["dnd", "do-not-disturb", "небеспокоить", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
							description="Меняет статус бота на \"Не беспокоить\".")
		@app_commands.default_permissions(manage_guild=True)
		async def donotdisturb(ctx):
			with open("assets/pfps/dnd.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
			if bot.get_guild(1142344574501658694).me.status != discord.Status.do_not_disturb:
				await ctx.reply("Теперь мой статус - `Не беспокоить`.", allowed_mentions=no_ping)
				await bot.change_presence(status=discord.Status.do_not_disturb)
			else:
				await ctx.reply("У меня и так статус `Не беспокоить`.")
		donotdisturb.error(pfp_ratelimit_msg)

		@bot.hybrid_command(aliases=["invis", "inv", "невидимка", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"],
							description="Меняет статус бота на \"Невидимка\".")
		@app_commands.default_permissions(manage_guild=True)
		async def invisible(ctx):
			with open("assets/pfps/offline.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
			if bot.get_guild(1142344574501658694).me.status != discord.Status.invisible:
				await ctx.reply("Теперь мой статус - `Невидимка`.", allowed_mentions=no_ping)
				await bot.change_presence(status=discord.Status.invisible)
			else:
				await ctx.reply("У меня и так статус `Невидимка`.")
		invisible.error(pfp_ratelimit_msg)

		@bot.hybrid_command(aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"],
							description="Показывает пинг бота.")
		async def ping(ctx):
			embed = discord.Embed(title="🏓 Понг!", color=no_color)
			embed.add_field(name=f'Мой пинг: {round(bot.latency*1000)}ms', value="", inline=True)
			await ctx.reply(embed=embed, allowed_mentions=no_ping)

		@bot.hybrid_command(aliases=["изменить", "эдит", "увше"],
							description="Изменяет заданное сообщение.")
		@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")
		@app_commands.default_permissions(manage_messages=True)
		async def edit(ctx, message:str, *, text:str):
			if ctx.message.reference == None:
				msg = await get_msg_by_id_arg(ctx, bot, message)
				await discord.Message.edit(self=msg,content=text)
			else:
				msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
				await discord.Message.edit(self=msg, content=message+" "+text)
		@edit.error
		async def edit_error(ctx, error: Exception):
			error_msg = str(error)
			if isinstance(error, commands.MissingRequiredArgument):
				await ctx.reply("❗ Не хватает аргументов.", allowed_mentions=no_ping)
			elif "403 Forbidden" in error_msg:
				await ctx.reply("❗ Не могу изменять чужие сообщения.", allowed_mentions=no_ping)
			elif "'NotFound'" in error_msg:
				await ctx.reply("❗ Не нашёл сообщения с таким айди.", allowed_mentions=no_ping)
			elif "'ValueError'" in error_msg:
				await ctx.reply("❗ Введён неверный айди.", allowed_mentions=no_ping)
			else:
				await ctx.reply(f"Шо та произошло но я не понял что. Подробности: `{error}`", allowed_mentions=no_ping)
