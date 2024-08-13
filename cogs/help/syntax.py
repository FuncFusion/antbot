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

	@commands.hybrid_command(
		aliases=["stx", "s", "ы", "ынтефч", "ыеч", "синтакс", "синтаксис", "сткс"],
		description="Показывает синтаксис указанной майнкрафт команды.",
		usage="`/syntax <команда>`",
		help="### Пример:\n`/syntax item`")
	@app_commands.describe(command="Команда из майнкрафта")

	async def syntax(self, ctx, *, command:str):
		syntaxes_dict = {}
		for syntax in syntaxes.keys():
			syntaxes_dict.update({syntax: []})
		command = closest_match(command, syntaxes_dict, 10)
		embed = discord.Embed(color=no_color)
		embed.description=f"## {Emojis.mcf_load} [/{command}](<https://minecraft.wiki/w/Commands/{command.replace(" ","#")}>)\n" + syntaxes[command]
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@syntax.error
	async def syntax_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите команду. Испльзуйте **слэш** команду </syntax:1250486582109274207>, где в автокомплите будет видно список команд."
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
			return [app_commands.Choice(name=command, value=command) for command in all_valid(curr, syntaxes)][:25]
		else:
			return offered_commands
