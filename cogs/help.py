import discord
from discord.ext import commands
from discord import app_commands

from settings import HELP_FORUM_ID
from utils.msg_utils import get_msg_by_id_arg
from utils.shortcuts import no_ping, no_color

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
				await ctx.response.send_message("❗ Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True, reference=ctx.message, allowed_mentions=no_ping)
			else:
				resolve_embed = discord.Embed(title="❎ Ветка закрыта без решения", color=no_color)
				await ctx.response.edit_message(embed=resolve_embed, view=None)
				await ctx.channel.edit(archived=True)
				self.stop()
		@discord.ui.button(label="Нет", style=discord.ButtonStyle.gray)
		async def cancel(self, ctx: discord.Interaction, button: discord.ui.Button):
			is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
			if ctx.user != ctx.channel.owner and not is_moderator:
				await ctx.response.send_message("❗ Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True, reference=ctx.message, allowed_mentions=no_ping)
			else:
				await ctx.message.delete()
				await ctx.response.send_message("❗ Пожалуйста, укажите в `resolve` ссылку на сообщение которое помголо \
					вам решить проблему и @упомяните людей которые помогли вам её решить".replace("\t", ""), view=None, ephemeral=True)
				self.stop()

	class Syntax:
		syntaxes = {}
		def read_syntaxes():
			syntaxes_path = "assets\\syntaxes"
			for filename in os.listdir(syntaxes_path):
				if filename.endswith(".md"):
					with open(os.path.join(syntaxes_path, filename), "r", encoding="utf-8") as file:
						HelpAdditionals.Syntax.syntaxes[filename.replace(".md", "")] = file.read()
		


HelpAdditionals.Syntax.read_syntaxes()
#


class HelpCommands(commands.Cog, name="Помощь"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["solve", "ыщдму", "куыщдму", "решено", "ресолв", "солв"],
						description="Архивирует ветку помощи при решении проблемы") 
	@app_commands.describe(solution="Сообщение которое помогло решить проблему (ссылка)",
						   helpers="Люди, которые помогли решить проблему")
	async def resolve(self, ctx, solution: str=None, *, helpers: str="None"):
		# Setting up variables
		heleprs_ids = [int(helepr_id) for helepr_id in re.findall(r"(?<=<@)([0-9]+)(?=>)", helpers)]
		helpers_mentions = re.findall(r"<@[0-9]+>", helpers)
		is_moderator = ctx.channel.permissions_for(ctx.author).manage_messages
		# Error handling
		if ctx.channel.parent_id != HELP_FORUM_ID:
			raise Exception("Channel is not help forum")
		elif ctx.author != ctx.channel.owner and not is_moderator:
			raise Exception("User not author/op")
		elif solution == None:
			# Building embed
			embed = discord.Embed(title="🤨 Погодите, вы уверены?", color=no_color,
				description="❗ Вы не указали ни сообщение, ни людей которые помогли решить проблему, \
				это заархивирует ветку без решения".replace("\t", ""))
			await ctx.send(embed=embed, view=HelpAdditionals.R_u_sure())
		elif type((solution:=await get_msg_by_id_arg(self, ctx, self.bot, solution))) != discord.Message:
			raise Exception("Wrong message")
		elif helpers == "None" or "@" not in helpers:
			raise Exception("Missing arg")
		# Building embed
		embed = discord.Embed(title="✅ Проблема решена", color=no_color)
		embed.add_field(name="Решение", value=f"🔗 {solution.jump_url}", inline=False)
		embed.add_field(name="Люди которые помогли" if len(helpers_mentions) >= 2 else "Человек который помог", 
			value=f"{"👥" if len(helpers_mentions) >= 2 else "👤"} {" ".join(helpers_mentions)}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
		await ctx.channel.edit(archived=True)
	@resolve.error
	async def resolve_error(self, ctx, error):
		error_msg = str(error)
		if "has no attribute 'parent_id'" in error_msg or "not help forum" in error_msg:
			await ctx.reply("❗ Эта команда работает только в ветках помощи", allowed_mentions=no_ping)
		elif "not author/op" in error_msg:
			await ctx.reply("❗ Вы не являетесь автором этой ветки либо модератором", allowed_mentions=no_ping)
		elif "Wrong message" in error_msg:
			await ctx.reply("❗ Неверная ссылка/айди сообщения", allowed_mentions=no_ping)
		elif "Missing arg" in error_msg:
			await ctx.reply("❗ Пожалуйста, @упомяните людей, которые помогли вам с проблемой", allowed_mentions=no_ping)
		
	@commands.hybrid_command(aliases=["stx", "ынтефч", "ыея", "синтакс", "синтаксис", "сткс"],
				  		description="Показывает синтакс введеной майнкрафт команды")
	@app_commands.describe(command="Команда с майнкрафта")
	async def syntax(self, ctx, command: str):
		HelpAdditionals.Syntax.read_syntaxes()
		#Bulding embed
		embed = discord.Embed(title=f"🖥 /{command}", color=no_color, 
			description=HelpAdditionals.Syntax.syntaxes[command])
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@syntax.error
	async def syntax_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply("❗ Пожалуйста, укажите команду", allowed_mentions=no_ping)
	@syntax.autocomplete("command")
	async def syntax_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		if curr == "":
			commands = list(HelpAdditionals.Syntax.syntaxes)
		else:
			commands = [command for command in HelpAdditionals.Syntax.syntaxes if curr in command]
		return [app_commands.Choice(name=command, value=command) for command in commands[:25]]
		

class HelpListeners(commands.Cog, name="no_help"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener("on_thread_create")
	async def help_in_chat(self, trd):
		if trd.parent_id == HELP_FORUM_ID:
			# Building embed
			embed = discord.Embed(title="📌 Ознакомься с правилами", color=no_color, 
				description=f"Если ещё не читал, прочти в закрепе ({links['pinned_help']}) рекомендации \
				к веткам помощи, и о том, как работают некоторые её аспекты. Следование всем рекомендациям \
				(особенно 4 пункту) поможет тебе получить наиболее эффективную помощь.".replace("\t", ""))
			#
			await trd.send(embed=embed)
			await trd.starter_message.pin()