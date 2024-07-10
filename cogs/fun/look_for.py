import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from Levenshtein import distance
from random import randint

from settings import LOOK_FOR_CHANNEL_ID

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate


class LookForCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="look-for",
		description="Создаёт пост в 🔍・поиск-тимы о поиске тиммейта")
	@app_commands.describe(game="Игра", details="Описание (айпи сервера/приглашение и тд)", image="Баннер к посту")

	async def look_for(self, ctx, game: str, details: str, image: discord.Attachment=None):
		embed = discord.Embed(title=f"{Emojis.spyglass} Ищу тиммейта для {game}", color=no_color)
		if not image:
			banners_count = {"minecraft": 3, "terraria": 0, "gartic": 0}
			games = {
				"minecraft": ["майнкрафт", "mc", "кубы", "говнокрафт"],
				"terraria": ["террария", "терка", "террка"],
				"gartic": ["гартик", "gartic phone", "сломанный телефон"]
			}
			validated_game = validate(game, games)
			if validated_game == None:
				game_banner = MISSING
			else:
				game_banner = discord.File(f"assets/game_banners/{validated_game}{randint(0, banners_count[validated_game])}.png",
				filename="banner.png")
				embed.set_image(url="attachment://banner.png")
		else:
			game_banner = await image.to_file(filename="banner.png")
			embed.set_image(url="attachment://banner.png")
		embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
		embed.add_field(name="Подробности", value=details, inline=False)
		embed.add_field(name=f"{Emojis.check} Присоединились", value="")
		embed.add_field(name=f"{Emojis.cross} Отклонили", value="")
		#
		LOOK_FOR_CHANNEL = await self.bot.fetch_channel(LOOK_FOR_CHANNEL_ID)
		lf_msg = await LOOK_FOR_CHANNEL.send(embed=embed, view=LookForView(), file=game_banner)
		await lf_msg.create_thread(name="Обсуждение")
		await ctx.response.send_message(f"{Emojis.check} Пост создан: {lf_msg.jump_url}", ephemeral=True)

	@look_for.error
	async def lf_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "game",
				"msg": f"{Emojis.exclamation_mark} Укажите игру, для которой ищите тиммейта"
			},
			{
				"contains": "details",
				"msg": f"{Emojis.exclamation_mark} Укажите подробности (айпи сервера/ссылка с приглашением и тд)"
			}
		])


class LookForView(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	async def response(ctx, action):
		embed = ctx.message.embeds[0]
		joined_users = embed.fields[1].value.split("\n")
		declined_users = embed.fields[2].value.split("\n")
		action_users_list = joined_users if action == "join" else declined_users
		opposite_users_list = declined_users if action == "join" else joined_users
		usr_ping = ctx.user.mention
		if usr_ping not in action_users_list:
			action_users_list.append(usr_ping)
		else:
			action_users_list.remove(usr_ping)
		if usr_ping in opposite_users_list:
			opposite_users_list.remove(usr_ping)
		embed.set_field_at(1, name=embed.fields[1].name, value="\n".join(joined_users))
		embed.set_field_at(2, name=embed.fields[2].name, value="\n".join(declined_users))
		await ctx.response.edit_message(embed=embed, attachments=[])
	
	@discord.ui.button(label="Присоединится", emoji=Emojis.check, custom_id="look-for:join")
	async def join(self, ctx, button):
		await LookForView.response(ctx, "join")
	
	@discord.ui.button(label="Отказатся", emoji=Emojis.cross, custom_id="look-for:decline")
	async def decline(self, ctx: discord.Interaction, button: discord.ui.Button):
		await LookForView.response(ctx, "decline")
	
	@discord.ui.button(label="Пингануть участников", emoji=Emojis.users, custom_id="look-for:ping-all")
	async def ping_all(self, ctx: discord.Interaction, button: discord.ui.Button):
		joined_users = ctx.message.embeds[0].fields[1].value.replace("\n", " ")
		if str(ctx.user.id) == ctx.message.embeds[0].author.icon_url.split("/")[4]: # post author's id
			if "<@" in joined_users:
				await ctx.message.thread.send(f"{joined_users} вас зовёт {ctx.user.mention}")
				await ctx.response.send_message("Участники пингануты", ephemeral=True)
			else:
				await ctx.response.send_message(f"{Emojis.exclamation_mark} Пока нет кого пинговать", ephemeral=True)
		else:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являеетесь автором поста", ephemeral=True)
	