import discord
from discord.ext import commands
from discord import app_commands

from settings import BOT_COMMANDS_CHANNEL_ID
from utils.shortcuts import no_ping

async def handle_errors(ctx, error, errors):
	error_msg = str(error)
	for case in errors:
		case_cost = len(case) - 1
		curr_score = 0
		if "exception" in case and isinstance(error, case["exception"]):
			curr_score += 1
		if "contains" in case and case["contains"] in error_msg:
			curr_score += 1
		#
		if curr_score == case_cost:
			await ctx.reply(case["msg"], allowed_mentions=no_ping, delete_after=(None if ctx.channel.id == \
				BOT_COMMANDS_CHANNEL_ID else 5))
			break
	else:
		await ctx.reply(f"Произошла непредвиденная ошибка, пожалуйста, сообщите о ней \
			<@536441049644793858> или <@567014541507035148>. Ошибка:\n`{error}`".replace("\t", ""),
			allowed_mentions=no_ping)
		print(error_msg)

class _MissingSentinel:
	__slots__ = ()

	def __eq__(self, other) -> bool:
		return False

	def __bool__(self) -> bool:
		return False

	def __hash__(self) -> int:
		return 0

	def __repr__(self):
		return '...'
	
	def __len__(self):
		return 0
	
	def __to_dict__(self):
		return {}
	
	def __iter__(self):
		return {}
	
	def __next__(self):
		raise StopIteration


MISSING: any = _MissingSentinel()