import discord
from discord.ext import commands
from discord import app_commands

from typing import List
import os

from utils import handle_errors, Emojis, split_msg, no_color, \
	no_ping, all_valid, closest_match, cache_message_author


syntaxes = {}
for filename in os.listdir("assets/syntaxes"):
	if filename.endswith(".md"):
		with open(f"assets/syntaxes/{filename}", "r", encoding="utf-8") as file:
			syntaxes[filename.replace(".md", "")] = file.read()

offered_commands = [app_commands.Choice(name=command, value=command) for command in sorted(list(syntaxes))[:25]]

class SyntaxCommand(commands.Cog):

	@commands.hybrid_command(
		aliases=["stx", "s", "ы", "ынтефч", "ыеч", "синтакс", "синтаксис", "сткс"],
		description="Показывает синтаксис указанной майнкрафт команды.",
		usage="`/syntax <команда>`",
		help="### Пример:\n`/syntax item`")
	@app_commands.describe(command="Команда из майнкрафта")

	async def syntax(self, ctx: commands.Context, *, command:str):
		syntaxes_dict = {}
		for syntax in syntaxes.keys():
			syntaxes_dict.update({syntax: []})
		command = " ".join(command.split()[:2])
		command = closest_match(command, syntaxes_dict, 10)
		if command == None:
			raise Exception("KeyError")
		msg = f"## {Emojis.mcf_load} [/{command}](<https://minecraft.wiki/w/Commands/{command.replace(" ","#")}>)\n" + syntaxes[command]
		parts = msg.split("\n---separator---\n")
		message_ids = []
		for part in parts:
			if parts.index(part) == 0:
				msg = await ctx.reply(part, allowed_mentions=no_ping)
				message_ids.append(msg.id)
			else:
				msg = await ctx.channel.send(part, allowed_mentions=no_ping)
				message_ids.append(msg.id)
		await cache_message_author(ctx.author.id, message_ids)

	@syntax.error
	async def syntax_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите команду. Используйте **слэш** команду </syntax:1250486582109274207>, где в автокомплите будет видно список команд."
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