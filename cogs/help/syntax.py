import discord
from discord.ext import commands
from discord import app_commands

from Levenshtein import distance
from typing import List
import os

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import all_valid, closest_match


syntaxes = {}
for filename in os.listdir("assets/syntaxes"):
	if filename.endswith(".md"):
		with open(f"assets/syntaxes/{filename}", "r", encoding="utf-8") as file:
			syntaxes[filename.replace(".md", "")] = file.read()

offered_commands = [app_commands.Choice(name=command, value=command) for command in list(syntaxes)[:25]]


class SyntaxCommand(commands.Cog):

	@commands.hybrid_command(aliases=["stx", "s", "ы", "ынтефч", "ыеч", "синтакс", "синтаксис", "сткс"],
		description="Показывает синтаксис введённой майнкрафт команды")
	@app_commands.describe(command="Команда из майнкрафта")

	async def syntax(self, ctx, *, command: str):
		command = closest_match(command, syntaxes, 8)
		embed = discord.Embed(color=no_color, 
			description=f"## {Emojis.mcf_load} [/{command}](<https://minecraft.wiki/w/Commands/{command.replace(" ","#")}>)\n" + syntaxes[command])
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@syntax.error
	async def syntax_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите команду"
			},
			{
				"exception": commands.CommandInvokeError,
				"msg": "Введена неверная команда"
			},
			{
				"contains": "KeyError",
				"msg": "Введена неверная команда"
			}
		])

	@syntax.autocomplete("command")
	async def syntax_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_commands
		if curr != "":
			offered_commands = [app_commands.Choice(name=command, value=command) for command in all_valid(curr, syntaxes)][:25]
		return offered_commands
