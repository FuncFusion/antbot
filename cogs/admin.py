import discord
from discord.ext import commands
from discord import app_commands



class AdminCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
							description="Отключает бота.")
		@app_commands.default_permissions(manage_guild=True)
		async def shutdown(ctx):
			await ctx.send("Отключаюсь...")
			await bot.close()

		@bot.hybrid_command(aliases=["on", "онлайн", "всети", "в-сети", "щтдшту", "щт"],
							description="Меняет статус бота на \"В сети\".")
		@app_commands.default_permissions(manage_guild=True)
		async def online(ctx):
			await ctx.send("Теперь мой статус - `В сети`.")
			await bot.change_presence(status=discord.Status.online)

		@bot.hybrid_command(aliases=["afk", "отошёл", "отойди", "айдл", "афк", "швду", "фал"],
							description="Меняет статус бота на \"Отошёл\".")
		@app_commands.default_permissions(manage_guild=True)
		async def idle(ctx):
			await ctx.send("Теперь мой статус - `Отошёл`.")
			await bot.change_presence(status=discord.Status.idle)

		@bot.hybrid_command(aliases=["dnd", "do-not-disturb", "небеспокоить", "не-беспокоить", "днд", "вщтщевшыегки", "втв", "вщ-тще-вшыегки"],
							description="Меняет статус бота на \"Не беспокоить\".")
		@app_commands.default_permissions(manage_guild=True)
		async def donotdisturb(ctx):
			await ctx.send("Теперь мой статус - `Не беспокоить`.")
			await bot.change_presence(status=discord.Status.do_not_disturb)

		@bot.hybrid_command(aliases=["invis", "inv", "невидимка", "невидимый", "инвизибл", "инвиз", "инв", "штмшышиду", "штмшы", "штм"],
							description="Меняет статус бота на \"Невидимка\".")
		@app_commands.default_permissions(manage_guild=True)
		async def invisible(ctx):
			await ctx.send("Теперь мой статус - `Невидимка`.")
			await bot.change_presence(status=discord.Status.invisible)

		@bot.hybrid_command(aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"],
							description="Показывает пинг бота.")
		async def ping(ctx):
			embed = discord.Embed(title="Понг!", color=discord.Colour.dark_embed())
			embed.add_field(name=f'Мой пинг: {round(bot.latency*1000)}ms', value="", inline=True)
			await ctx.send(embed=embed)

		@bot.hybrid_command(aliases=["изменить", "эдит", "увше"],
							description="Изменяет заданное сообщение.")
		@app_commands.describe(message="Сообщение, которое будет изменяться.", text="Текст, на который изменится сообщение.")
		@app_commands.default_permissions(manage_messages=True)
		async def edit(ctx, message:str=None, *, text:str=""):
			if message == None:
				await ctx.send("Не хватает аргументов.")
			else:
				try:
					if ctx.message.reference == None:
						id = (message.split("/")[-2:])
						msg = None
						if len(id) == 2 or (len(id:=id[0].split("-")) == 2): 
							chnl = bot.get_channel(int(id[0]))
							msg = await chnl.fetch_message(int(id[1]))
						else:
							msg = await ctx.channel.fetch_message(int(id[-1]))
						await discord.Message.edit(self=msg,content=text)
					else:
						msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
						await discord.Message.edit(self=msg, content=message+" "+text)
				except Exception as e:
					if str(e).startswith('403'):
						await ctx.send(f"Не могу изменять чужие сообщения.")
					elif str(e).startswith('404'):
						await ctx.send(f"Не нашёл сообщения с таким айди.")
					elif str(e).startswith('invalid literal for int()'):
						await ctx.send(f"Введён неверный айди.")
					else:
						await ctx.send(f"Не хватает аргументов.")
