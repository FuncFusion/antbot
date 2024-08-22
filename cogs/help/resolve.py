import discord
from discord.ext import commands
from discord import app_commands

from settings import HELP_FORUM_ID, SOLVED_TAG

from re import findall

from utils.general import handle_errors
from utils.msg_utils import Emojis, get_msg_by_id_arg
from utils.shortcuts import no_color, no_ping


class ResolveCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["solve", "ыщдму", "куыщдму", "решено", "ресолв", "солв"],
		description="Архивирует ветку помощи при решении проблемы.",
		usage="`/resolve [cсылка|айди сообщения с решением проблемы] [пользователь(и), которые помогли]`",
		help="Используйте факьюшку `?resolve`, чтоб узнать больше о том, как правильно использовать эту команду.\n### Пример:\n`/resolve https://discord.com/channels/1097272592676700250/1262127423294672906/1262127471256403968 <@536441049644793858>`") 
	@app_commands.describe(solution="Сообщение, которое помогло решить проблему (ссылка)",
		helpers="Люди, которые помогли решить проблему")

	async def resolve(self, ctx, solution: str=None, *, helpers: str="None"):
		# Args from reply
		if ctx.message.reference and not solution:
			reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			solution = reference.jump_url
			helpers = reference.author.mention
		#
		helpers_mentions = findall(r"<@[0-9]+>", helpers)
		is_moderator = ctx.channel.permissions_for(ctx.author).manage_messages
		# Error handling
		if ctx.channel.parent_id != HELP_FORUM_ID:
			raise Exception("Channel is not help forum")
		elif ctx.author != ctx.channel.owner and not is_moderator:
			raise Exception("User not author/op")
		elif solution == None and not ctx.message.refernce:
			embed = discord.Embed(title="🤨 Погодите, вы уверены?", color=no_color,
				description=f"{Emojis.exclamation_mark} Вы не указали ни сообщение, ни "
				"людей которые помогли решить проблему, это заархивирует ветку без решения")
			await ctx.send(embed=embed, view=R_u_sure())
			return
		elif type((solution:=await get_msg_by_id_arg(self, ctx, self.bot, solution))) != discord.Message:
			raise Exception("Wrong message")
		elif helpers == "None" or "@" not in helpers:
			raise Exception("Missing arg")
		# Building embed
		embed = discord.Embed(title=f"{Emojis.check} Проблема решена", color=no_color)
		embed.add_field(name="Решение", value=f"{Emojis.link} {solution.jump_url}", inline=False)
		embed.add_field(name="Люди, которые помогли" if len(helpers_mentions) >= 2 else "Человек, который помог", 
			value=f"{Emojis.user if len(helpers_mentions) < 2 else Emojis.users} {" ".join(helpers_mentions)}")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
		await ctx.channel.add_tags(SOLVED_TAG)
		await ctx.channel.edit(archived=True)

	@resolve.error
	async def resolve_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "has no attribute 'parent_id'",
				"msg": "Эта команда работает только в ветках помощи"
			},
			{
				"contains": "not help forum",
				"msg": "Эта команда работает только в ветках помощи"
			},
			{
				"contains": "not author/op",
				"msg": "Вы не являетесь автором этой ветки либо модератором"
			},
			{
				"contains": "Wrong message",
				"msg": "Неверная ссылка/айди сообщения"
			},
			{
				"contains": "Missing arg",
				"msg": f"Пожалуйста, @упомяните людей, которые помогли вам с проблемой"
			}
		])


class R_u_sure(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label="Да", style=discord.ButtonStyle.red, custom_id="resolve:submit")
	async def submit(self, ctx: discord.Interaction, button: discord.ui.Button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором", ephemeral=True, allowed_mentions=no_ping)
		else:
			await ctx.message.delete()
			resolve_embed = discord.Embed(title=f"{Emojis.cross} Ветка закрыта без решения", color=no_color)
			await ctx.response.send_message(embed=resolve_embed)
			await ctx.channel.edit(archived=True)
			self.stop()
	
	@discord.ui.button(label="Нет", style=discord.ButtonStyle.gray, custom_id="resolve:cancel")
	async def cancel(self, ctx: discord.Interaction, button: discord.ui.Button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором", ephemeral=True, allowed_mentions=no_ping)
		else:
			await ctx.message.delete()
			await ctx.response.send_message(content=f"{Emojis.exclamation_mark} Пожалуйста, укажите в "
				"`soultion` команды </resolve:1250486582109274206> ссылку на сообщение которое помголо "
				"вам решить проблему, и @упомяните в `helpers` людей которые помогли вам её решить", ephemeral=True)
			self.stop()
		