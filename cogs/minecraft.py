import discord
from discord.ext import commands
from discord import app_commands
import re

from utils.highlighter.main import Highlighter as hl
from utils.fake_user import fake_send

code_block_content_re = r"```[a-zA-Z+]+\n|```\n?"

class MinecraftCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["hl", "рд","хайлайт", "хл"],
							description="Подсвечивает синтакс для mcfunction")
		async def highlight(ctx, *, command:str="default_variant"):
			# Setting up vars
			message = ""
			if command == "default_variant":
				if (reply:=ctx.message.reference) != None:
					reply_message = await ctx.channel.fetch_message(reply.message_id)
					reply_message = reply_message.content
					if "```" in reply_message:
						for code_block in re.split(code_block_content_re, reply_message)[1::2]:
							message += f"```ansi\n{hl.highlight(code_block)}```"
					else:
						message += f"```ansi\n{hl.highlight(reply_message)}```"
				else:
					await ctx.send("Не хватает функции/ответа на сообщение с функцией", reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
					return None
			else:
				if "```" in command:
					for code_block in re.split(code_block_content_re, command)[1::2]:
						message += f"```ansi\n{hl.highlight(code_block)}```"
				else:
					message += f"```ansi\n{hl.highlight(command)}```"
			# Building embed
			embed = discord.Embed(title="Подсвеченная функция" if message.count("```") == 2 else "Подсвеченные функции", color=discord.Colour.dark_embed(), description=message)
			await ctx.send(embed=embed, reference=ctx.message, allowed_mentions=discord.AllowedMentions.none())
	
		@bot.tree.context_menu(name="🌈Подсветить функцию")
		async def highlight_ctxmenu(interaction: discord.Interaction, message:discord.Message):
			# Setting up variables
			code_block_re = r"```[^`]+```"
			if interaction.user == message.author:
				mcfed_message = " " + message.content
				if "```" in message.content:
					for code_block, code_block_content in zip(re.findall(code_block_re, message.content), re.split(code_block_content_re, message.content)[1::2]):
						mcfed_message = mcfed_message.replace(code_block, f"```ansi\n{hl.highlight(code_block_content)}```")
				else:
					mcfed_message = f"```ansi\n{hl.highlight(message.content)}```"
				await fake_send(interaction.user, interaction.channel, content=mcfed_message)
				await interaction.response.send_message("Сообщение с функцией подсвечено", ephemeral=True)
				await message.delete()
			else:
				mcfed_message = ""
				if "```" in message.content:
					for code_block in re.split(code_block_content_re, message.content)[1::2]:
						mcfed_message += f"```ansi\n{hl.highlight(code_block)}```"
				else:
					mcfed_message += f"```ansi\n{hl.highlight(message.content)}```"
				# Building embed
				embed = discord.Embed(title="Подсвеченная функция" if message.content.count("```") == 2 else "Подсвеченные функции", color=discord.Colour.dark_embed(), description=mcfed_message)
				await interaction.response.send_message(embed=embed)
