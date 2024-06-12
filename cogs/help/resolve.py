import discord
from discord.ext import commands
from discord import app_commands

from settings import HELP_FORUM_ID

from re import findall

from utils.general import handle_errors
from utils.msg_utils import Emojis, get_msg_by_id_arg
from utils.shortcuts import no_color, no_ping


class R_u_sure(discord.ui.View):
	def __init__(self):
		super().__init__()
	@discord.ui.button(label="Да", style=discord.ButtonStyle.red)
	async def submit(self, ctx: discord.Interaction, button: discord.ui.Button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True, reference=ctx.message, allowed_mentions=no_ping)
		else:
			resolve_embed = discord.Embed(title=f"{Emojis.cross} Ветка закрыта без решения", color=no_color)
			await ctx.response.edit_message(embed=resolve_embed, view=None)
			await ctx.channel.edit(archived=True)
			self.stop()
	@discord.ui.button(label="Нет", style=discord.ButtonStyle.gray)
	async def cancel(self, ctx: discord.Interaction, button: discord.ui.Button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором", view=None, ephemeral=True, reference=ctx.message, allowed_mentions=no_ping)
		else:
			await ctx.message.delete()
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Пожалуйста, укажите в `resolve` ссылку на сообщение которое помголо \
				вам решить проблему и @упомяните людей которые помогли вам её решить".replace("\t", ""), view=None, ephemeral=True)
			self.stop()


class ResolveCommand(commands.Cog):

	@commands.hybrid_command(aliases=["solve", "ыщдму", "куыщдму", "решено", "ресолв", "солв"],
		description="Архивирует ветку помощи при решении проблемы") 
	@app_commands.describe(solution="Сообщение которое помогло решить проблему (ссылка)",
		helpers="Люди, которые помогли решить проблему")

	async def resolve(self, ctx, solution: str=None, *, helpers: str="None"):
		heleprs_ids = [int(helepr_id) for helepr_id in findall(r"(?<=<@)([0-9]+)(?=>)", helpers)]
		helpers_mentions = findall(r"<@[0-9]+>", helpers)
		is_moderator = ctx.channel.permissions_for(ctx.author).manage_messages
		# Error handling
		if ctx.channel.parent_id != HELP_FORUM_ID:
			raise Exception("Channel is not help forum")
		elif ctx.author != ctx.channel.owner and not is_moderator:
			raise Exception("User not author/op")
		elif solution == None:
			# Building embed
			embed = discord.Embed(title="🤨 Погодите, вы уверены?", color=no_color,
				description=f"{Emojis.exclamation_mark} Вы не указали ни сообщение, ни людей которые помогли решить проблему, \
				это заархивирует ветку без решения".replace("\t", ""))
			await ctx.send(embed=embed, view=R_u_sure())
		elif type((solution:=await get_msg_by_id_arg(self, ctx, self.bot, solution))) != discord.Message:
			raise Exception("Wrong message")
		elif helpers == "None" or "@" not in helpers:
			raise Exception("Missing arg")
		# Building embed
		embed = discord.Embed(title=f"{Emojis.check} Проблема решена", color=no_color)
		embed.add_field(name="Решение", value=f"{Emojis.link} {solution.jump_url}", inline=False)
		embed.add_field(name="Люди которые помогли" if len(helpers_mentions) >= 2 else "Человек который помог", 
			value=f"{Emojis.user if len(helpers_mentions) >= 2 else Emojis.users} {" ".join(helpers_mentions)}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
		await ctx.channel.edit(archived=True)

	@resolve.error
	async def resolve_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "has no attribute 'parent_id'",
				"msg": f"{Emojis.exclamation_mark} Эта команда работает только в ветках помощи"
			},
			{
				"contains": "not help forum",
				"msg": f"{Emojis.exclamation_mark} Эта команда работает только в ветках помощи"
			},
			{
				"contains": "not author/op",
				"msg": f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором"
			},
			{
				"contains": "Wrong message",
				"msg": f"{Emojis.exclamation_mark} Неверная ссылка/айди сообщения"
			},
			{
				"contains": "Missing arg",
				"msg": f"{Emojis.exclamation_mark} Пожалуйста, @упомяните людей, которые помогли вам с проблемой"
			}
		])
		