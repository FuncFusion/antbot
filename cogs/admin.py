import discord
from discord.ext import commands
from discord import app_commands
from utils.msg_utils import get_msg_by_id_arg

async def pfp_ratelimit_msg(ctx):
	await ctx.send("Тихо, тихо, не могу так быстро менять аватарку. Попробуй позже", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
	
class AdminCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
							description="Отключает бота.")
		@app_commands.default_permissions(manage_guild=True)
		async def shutdown(ctx):
			try:
				with open("assets/pfps/offline.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
				await ctx.send("Отключаюсь...", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
				await bot.close()
			except Exception:
				await pfp_ratelimit_msg(ctx)

		@bot.hybrid_command(aliases=["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
							description="Меняет статус бота на \"В сети\".")
		@app_commands.default_permissions(manage_guild=True)
		async def online(ctx):
			try:
				with open("assets/pfps/online.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
				await ctx.send("Теперь мой статус - `В сети`.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.online)
			except Exception:
				await pfp_ratelimit_msg(ctx)

		@bot.hybrid_command(aliases=["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
							description="Меняет статус бота на \"Отошёл\".")
		@app_commands.default_permissions(manage_guild=True)
		async def idle(ctx):
			try:
				with open("assets/pfps/idle.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
				await ctx.send("Теперь мой статус - `Отошёл`.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.idle)
			except Exception:
				await pfp_ratelimit_msg(ctx)

		@bot.hybrid_command(aliases=["dnd", "do-not-disturb", "небеспокоить", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
							description="Меняет статус бота на \"Не беспокоить\".")
		@app_commands.default_permissions(manage_guild=True)
		async def donotdisturb(ctx):
			try:
				with open("assets/pfps/dnd.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
				await ctx.send("Теперь мой статус - `Не беспокоить`.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.do_not_disturb)
			except Exception:
				await pfp_ratelimit_msg(ctx)

		@bot.hybrid_command(aliases=["invis", "inv", "невидимка", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"],
							description="Меняет статус бота на \"Невидимка\".")
		@app_commands.default_permissions(manage_guild=True)
		async def invisible(ctx):
			try:
				with open("assets/pfps/offline.png", "rb") as file:
					await bot.user.edit(avatar=file.read())
				await ctx.send("Теперь мой статус - `Невидимка`.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
				await bot.change_presence(status=discord.Status.invisible)
			except Exception:
				await pfp_ratelimit_msg(ctx)

		@bot.hybrid_command(aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"],
							description="Показывает пинг бота.")
		async def ping(ctx):
			embed = discord.Embed(title="Понг!", color=discord.Colour.dark_embed())
			embed.add_field(name=f'Мой пинг: {round(bot.latency*1000)}ms', value="", inline=True)
			await ctx.send(embed=embed, reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())

		@bot.hybrid_command(aliases=["изменить", "эдит", "увше"],
							description="Изменяет заданное сообщение.")
		@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")
		@app_commands.default_permissions(manage_messages=True)
		async def edit(ctx, message:str=None, *, text:str=""):
			if message == None:
				await ctx.send("Не хватает аргументов.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
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
						await ctx.send(f"Не могу изменять чужие сообщения.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
					elif str(msg).startswith('404'):
						await ctx.send("Не нашёл сообщения с таким айди.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
					elif str(msg).startswith('invalid literal for int()'):
						await ctx.send("Введён неверный айди.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
					else:
						await ctx.send("Не хватает аргументов.", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
