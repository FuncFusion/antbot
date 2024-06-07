import discord
from discord.ext import commands
from discord import app_commands

from settings import LOOK_FOR_ID

from Levenshtein import distance
from random import randint

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping


class LookForCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(name="look-for", aliases=["lf", "дщщл-ащк", "да", "ищу-тиммейта"],
		description="Создаёт пост в 🔍・поиск-тимы о поиске тиммейта")
	@app_commands.describe(game="Игра", details="Описание (айпи сервера/приглашение и тд)")

	async def look_for(self, ctx, game: str, *, details: str):
		games = {
			"minecraft": {
				"banners_count": 3,
				"ru_name": "майнкрафт",
				"accusative": "майнкрафта"
			},
			"terraria": {
				"banners_count": 0,
				"ru_name": "террария",
				"accusative": "террарии"
			},
			"gartic": {
				"banners_count": 0,
				"ru_name": "гартик",
				"accusative": "гартика"
			},
			"other": {
				"banners_count": 0,
				"ru_name": game,
				"accusative": game
			}
		}
		for game_name in games:
			if distance(game, game_name) <= len(game_name)/2 \
				or distance(game, games[game_name]["ru_name"]) <= len(games[game_name]["ru_name"])/2:
				game = game_name
				break
		else:
			game = "other"
		look_for_channel = await self.bot.fetch_channel(LOOK_FOR_ID)
		embed = discord.Embed(title=f"{Emojis.spyglass} Ищу тиммейта для {games[game]["accusative"]}", color=no_color)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
		embed.add_field(name="Подробности", value=details, inline=False)
		embed.add_field(name=f"{Emojis.check} Присоединились", value="")
		embed.add_field(name=f"{Emojis.cross} Отклонили", value="")
		if game in games:
			game_banner = discord.File(f"assets/game_banners/{game}{randint(0, games[game]["banners_count"])}.png", filename="say_gex.png")
			embed.set_image(url="attachment://say_gex.png")
		lf_msg = await look_for_channel.send(embed=embed, view=LookForView(), file=game_banner)
		await lf_msg.create_thread(name="Обсуждение", reason="Auto-thread for look for teammate")
		await ctx.reply(f"{Emojis.check} Пост создан: {lf_msg.jump_url}", allowed_mentions=no_ping)

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
		joined_users = ctx.message.embeds[0].fields[1].value.split("\n")
		if str(ctx.user.id) == ctx.message.embeds[0].author.icon_url.split("/")[4]: # post author's id
			if joined_users != []:
				await ctx.message.thread.send(f"{' '.join(joined_users)} вас зовёт {ctx.user.mention}")
				await ctx.response.send_message("Участники пингануты", ephemeral=True)
			else:
				await ctx.response.send_message(f"{Emojis.exclamation_mark} Пока нет кого пинговать", ephemeral=True)
		else:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являеетесь автором поста", ephemeral=True)
	