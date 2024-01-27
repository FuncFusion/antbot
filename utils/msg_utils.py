import discord
from discord.ext import commands
from discord import app_commands

async def get_msg_by_id_arg(ctx, bot, arg:str):
	try:
		id = (arg.split("/")[-2:])
		if len(id) == 2 or (len(id:=id[0].split("-")) == 2): 
			chnl = bot.get_channel(int(id[0]))
			msg = await chnl.fetch_message(int(id[1]))
		else:
			msg = await ctx.channel.fetch_message(int(id[-1]))
		return msg
	except Exception as e:
		if str(e).startswith('404'):
			await ctx.send("Не нашёл сообщения с таким айди.")
		elif str(e).startswith('invalid literal for int()'):
			await ctx.send("Введён неверный айди.")
		else:
			await ctx.send(f"{e}")
		return 'id_error'