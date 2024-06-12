import discord
from discord.ext import commands
from discord import app_commands

from Levenshtein import distance
from typing import List
import os

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


syntaxes = {}
def read_syntaxes():
	syntaxes_path = "assets\\syntaxes"
	for filename in os.listdir(syntaxes_path):
		if filename.endswith(".md"):
			with open(os.path.join(syntaxes_path, filename), "r", encoding="utf-8") as file:
				syntaxes[filename.replace(".md", "")] = file.read()
read_syntaxes()
		

class SyntaxCommand(commands.Cog):

	@commands.hybrid_command(aliases=["stx", "ынтефч", "ыея", "синтакс", "синтаксис", "сткс"],
		description="Показывает синтакс введеной майнкрафт команды")
	@app_commands.describe(command="Команда с майнкрафта")

	async def syntax(self, ctx, command: str):
		embed = discord.Embed(color=no_color, 
			description=f"# {Emojis.mcf_load} [/{command}](<https://minecraft.wiki/w/Commands/{command}>)\n" + syntaxes[command])
		await ctx.reply(embed=embed, allowed_mentions=no_ping)

	@syntax.error
	async def syntax_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Пожалуйста, укажите команду"
			}
		])

	@syntax.autocomplete("command")
	async def syntax_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		if curr == "":
			commands = list(syntaxes)
		else:
			commands = [command for command in syntaxes if curr in command or distance(curr, command) <= len(command)/2]
		return [app_commands.Choice(name=command, value=command) for command in commands[:25]]
