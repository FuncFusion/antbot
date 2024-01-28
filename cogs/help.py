import discord
from discord.ext import commands
from discord import app_commands

from settings import HELP_FORUM_ID
from utils.msg_utils import get_msg_by_id_arg

import re
import os
from typing import List

links = {
	"pinned_help": "https://discord.com/channels/914772142300749854/1021488153909018704"
}


class HelpAdditionals:
	class R_u_sure(discord.ui.View):
		def __init__(self):
			super().__init__()
		@discord.ui.button(label="Да", style=discord.ButtonStyle.red)
		async def submit(self, ctx: discord.Interaction, button: discord.ui.Button):
			is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
			if ctx.user != ctx.channel.owner and not is_moderator:
				await ctx.response.send_message("Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True)
			else:
				resolve_embed = discord.Embed(title="❎ Ветка закрыта без решения", color=discord.Color.dark_embed())
				await ctx.response.edit_message(embed=resolve_embed, view=None)
				await ctx.channel.edit(locked=True)
				self.stop()
		@discord.ui.button(label="Нет", style=discord.ButtonStyle.gray)
		async def cancel(self, ctx: discord.Interaction, button: discord.ui.Button):
			is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
			if ctx.user != ctx.channel.owner and not is_moderator:
				await ctx.response.send_message("Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True)
			else:
				await ctx.message.delete()
				await ctx.response.send_message("Пожалуйста, укажите в `resolve` ссылку на сообщение которое помголо \
					вам решить проблему и @упомяните людей которые помогли вам её решить".replace("\t", ""), view=None, ephemeral=True)
				self.stop()

	class Syntax:
		syntaxes = {}
		def read_syntaxes():
			syntaxes_path = "assets\\syntaxes"
			for filename in os.listdir(syntaxes_path):
				if filename.endswith(".md"):
					with open(os.path.join(syntaxes_path, filename), "r") as file:
						HelpAdditionals.Syntax.syntaxes[filename.replace(".md", "")] = file.read()
		


HelpAdditionals.Syntax.read_syntaxes()
#


class HelpCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["solve", "ыщдму", "куыщдму", "решено", "ресолв", "солв"],
							description="Архивирует ветку помощи при решении проблемы") 
		@app_commands.describe(solution="Сообщение которое помогло решить проблему (ссылка)",
							   helpers="Люди, которые помогли решить проблему")
		async def resolve(ctx, solution: str=None, *, helpers: str=None):
			is_moderator = ctx.channel.permissions_for(ctx.author).manage_messages
			# Error handling
			if type(ctx.channel) != discord.threads.Thread:
				await ctx.send("Эта команда работает только в ветках помощи")
			elif ctx.channel.parent_id != HELP_FORUM_ID:
				await ctx.send("Эта команда работает только в ветках помощи")
			elif ctx.author != ctx.channel.owner and not is_moderator:
				await ctx.send("Вы не являетесь автором этой ветки либо модератором")
			elif solution == None:
				# Building embed
				embed = discord.Embed(title="🤨 Погодите, вы уверены?", color=discord.Color.dark_embed(),
					description="Вы не указали ни сообщение ни людей которые помогли решить проблему, \
					это заархивирует ветку без решения".replace("\t", ""))
				await ctx.send(embed=embed, view=HelpAdditionals.R_u_sure())
			elif type((solution:=await get_msg_by_id_arg(ctx, bot, solution))) != discord.Message:
				await ctx.send("Неверная ссылка/айди сообщения")
			elif helpers == None:
				await ctx.send("Пожалйста, @упомяните людей которые помогли вам с проблемой")
			else:
				# Setting up variables
				heleprs_ids = [int(helepr_id) for helepr_id in re.findall(r"(?<=<@)([0-9]+)(?=>)", helpers)]
				helpers_mentions = re.findall(r"<@[0-9]+>", helpers)
				# Building embed
				embed = discord.Embed(title="✅ Проблема решена", color=discord.Color.dark_embed())
				embed.add_field(name="Решение", value=f"🔗 {solution.jump_url}", inline=False)
				embed.add_field(name="Люди которые помогли" if len(helpers_mentions) >= 2 else "Человек который помог", 
					value=f"{"👥" if len(helpers_mentions) >= 2 else "👤"} {" ".join(helpers_mentions)}")
				await ctx.send(embed=embed)
				await ctx.channel.edit(locked=True)
		
		@bot.hybrid_command(aliases=["stx", "ынтефч", "ыея", "синтакс", "синтаксис", "сткс"],
					  		description="Показывает синтакс введеной майнкрафт команды")
		@app_commands.describe(command="Команда с майнкрафта")
		async def syntax(ctx, command: str=None):
			# Handling errors
			if command == None:
				await ctx.send("Пожалуйста, укажите команду")
			else:
				#Bulding embed
				embed = discord.Embed(title=f"🖥 /{command}", color=discord.Color.dark_embed(), 
					description=HelpAdditionals.Syntax.syntaxes[command])
				await ctx.send(embed=embed)
		@syntax.autocomplete("command")
		async def syntax_autocomplete(ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
			if curr == "":
				commands = list(HelpAdditionals.Syntax.syntaxes)
			else:
				commands = [command for command in HelpAdditionals.Syntax.syntaxes if curr in command]
			return [app_commands.Choice(name=command, value=command) for command in commands[:25]]
		

class HelpListeners(commands.Cog):
	def __init__(self, bot):
	
		@bot.listen("on_thread_create")
		async def help_in_chat(trd):
			if trd.parent_id == HELP_FORUM_ID:
				# Building embed
				embed = discord.Embed(title="📌 Ознакомся с правилами", color=discord.Color.dark_embed(), 
					description=f"Если ещё не читал, прочти в закрепе ({links['pinned_help']}) рекомендации \
					к веткам помощи, и о том, как работают некоторые её аспекты. Следование всем рекомендациям \
					поможет тебе получить как можно более эффективную помощь.".replace("\t", ""))
				#
				await trd.send(embed=embed)