import discord
from discord.ext import commands
from discord import app_commands
from utils.msg_utils import get_msg_by_id_arg
from utils.emojis import Emojis

async def pfp_ratelimit_msg(ctx):
	await ctx.reply(f"{Emojis.mojo} Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже", allowed_mentions=discord.AllowedMentions.none())
	
class AdminCommands(commands.Cog):
	def __init__(self, bot):
		
		@bot.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
							description="Отключает бота.")
		@app_commands.default_permissions(manage_guild=True)
		async def shutdown(ctx):
			try:
				with open("assets/pfps/offline.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
			except Exception:
				await pfp_ratelimit_msg(ctx)
			await ctx.reply("Отключаюсь... 😴", allowed_mentions=discord.AllowedMentions.none())
			await bot.close()

		@bot.hybrid_command(aliases=["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
							description="Меняет статус бота на \"В сети\".")
		@app_commands.default_permissions(manage_guild=True)
		async def online(ctx):
			try:
				with open("assets/pfps/online.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
			except Exception:
				await pfp_ratelimit_msg(ctx)
			if bot.get_guild(1142344574501658694).me.status != discord.Status.online:
				await ctx.reply("Теперь мой статус - `В сети`.", allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.online)
			else:
				await ctx.reply("У меня и так статус `В сети`.")

		@bot.hybrid_command(aliases=["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
							description="Меняет статус бота на \"Отошёл\".")
		@app_commands.default_permissions(manage_guild=True)
		async def idle(ctx):
			try:
				with open("assets/pfps/idle.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
			except Exception:
				await pfp_ratelimit_msg(ctx)
			if bot.get_guild(1142344574501658694).me.status != discord.Status.idle:
				await ctx.reply("Теперь мой статус - `Отошёл`.", allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.idle)
			else:
				await ctx.reply("У меня и так статус `Отошёл`.")

		@bot.hybrid_command(aliases=["dnd", "do-not-disturb", "небеспокоить", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
							description="Меняет статус бота на \"Не беспокоить\".")
		@app_commands.default_permissions(manage_guild=True)
		async def donotdisturb(ctx):
			try:
				with open("assets/pfps/dnd.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
			except Exception:
				await pfp_ratelimit_msg(ctx)
			if bot.get_guild(1142344574501658694).me.status != discord.Status.do_not_disturb:
				await ctx.reply("Теперь мой статус - `Не беспокоить`.", allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.do_not_disturb)
			else:
				await ctx.reply("У меня и так статус `Не беспокоить`.")

		@bot.hybrid_command(aliases=["invis", "inv", "невидимка", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"],
							description="Меняет статус бота на \"Невидимка\".")
		@app_commands.default_permissions(manage_guild=True)
		async def invisible(ctx):
			try:
				with open("assets/pfps/offline.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
			except Exception:
				await pfp_ratelimit_msg(ctx)
			if bot.get_guild(1142344574501658694).me.status != discord.Status.invisible:
				await ctx.reply("Теперь мой статус - `Невидимка`.", allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.invisible)
			else:
				await ctx.reply("У меня и так статус `Невидимка`.")

		@bot.hybrid_command(aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"],
							description="Показывает пинг бота.")
		async def ping(ctx):
			embed = discord.Embed(title="🏓 Понг!", color=discord.Colour.dark_embed())
			embed.add_field(name=f'Мой пинг: {round(bot.latency*1000)}ms', value="", inline=True)
			await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())

		@bot.hybrid_command(aliases=["изменить", "эдит", "увше"],
							description="Изменяет заданное сообщение.")
		@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")
		@app_commands.default_permissions(manage_messages=True)
		async def edit(ctx, message:str=None, *, text:str=""):
			if message == None:
				await ctx.reply("❗ Не хватает аргументов.", allowed_mentions=discord.AllowedMentions.none())
			else:
				try:
					if ctx.message.reference == None:
						msg = await get_msg_by_id_arg(ctx, bot, message)
						await discord.Message.edit(self=msg,content=text)
					else:
						msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
						await discord.Message.edit(self=msg, content=message+" "+text)
				except Exception as e:
					if str(e).startswith('403'):
						await ctx.reply(f"❗ Не могу изменять чужие сообщения.", allowed_mentions=discord.AllowedMentions.none())
					elif str(msg).startswith('404'):
						await ctx.reply("❗ Не нашёл сообщения с таким айди.", allowed_mentions=discord.AllowedMentions.none())
					elif str(msg).startswith('invalid literal for int()'):
						await ctx.reply("❗ Введён неверный айди.", allowed_mentions=discord.AllowedMentions.none())
					else:
						await ctx.reply("❗ Не хватает аргументов.", allowed_mentions=discord.AllowedMentions.none())
