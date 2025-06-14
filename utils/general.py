import discord
from discord.ext import commands
from discord.ext.commands import hybrid

from typing import Union

from settings import BOT_COMMANDS_CHANNEL_ID
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping


# Generic error messages
missing_argument = "Не указан обязательный аргумент"
missing_argument_addition = (". Рекомендую использовать команду в слэш виде "
                    		 "({}) что бы ознакомиться со всеми ее параметрами")
unknown_error = ("Произошла непредвиденная ошибка, пожалуйста, сообщите о ней "
                 "<@536441049644793858> или <@567014541507035148>. Ошибка:\n`{}`")

async def handle_errors(
		ctx: Union[commands.Context, discord.Interaction], 
		error, 
		errors
	):

	if isinstance(ctx, discord.Interaction):
		ctx = await commands.Context.from_interaction(ctx)

	async def send(msg):
		emoji = Emojis.exclamation_mark if not case['msg'].startswith("<") else ''
		if ctx.interaction:
			await ctx.interaction.response.send_message(f"{emoji}{msg}", allowed_mentions=no_ping, ephemeral=True)
		else:
			await ctx.reply(f"{emoji}{msg}", allowed_mentions=no_ping, delete_after=(None if ctx.channel.id == \
				BOT_COMMANDS_CHANNEL_ID else 5))

	error_msg = str(error)

	for case in errors:
		case_cost = len(case) - 1
		curr_score = 0
		if "exception" in case and isinstance(error, case["exception"]):
			curr_score += 1
		if "contains" in case and case["contains"] in error_msg:
			curr_score += 1
		#
		if curr_score >= case_cost:
			await send(case["msg"])
			break

	else:
		# Common errors
		if type(error) in (commands.MissingRequiredAttachment, commands.MissingRequiredArgument):
			command_mention = [cmd.mention for cmd in await ctx.bot.tree.fetch_commands() if cmd.name == ctx.command.name]
			message = missing_argument
			if command_mention:
				message += missing_argument_addition.format(command_mention[0])
			await send(message)
		else:
			await send(unknown_error.format(error))
			print(error_msg)
