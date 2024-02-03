import discord
from discord.ext import commands
from discord import app_commands
from utils.shortcuts import no_ping

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
		return e
	
async def unknown_error(ctx, error):
	await ctx.reply(f"Произошла непредвиденная ошибка, пожалуйста, сообщите о ней \
					<@536441049644793858> или <@567014541507035148>. Ошибка:\n`{error}`", allowed_mentions=no_ping).replace("\t", "")
	print(type(error), error)