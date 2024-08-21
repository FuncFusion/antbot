import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from pymongo.mongo_client import MongoClient
from random import randint

from settings import LOOK_FOR_CHANNEL_ID, MONGO_URI
from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate

db = MongoClient(MONGO_URI).antbot.look_for


class LookForCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="look-for",
		description="Создаёт пост в 🔍・поиск-тимы о поиске тиммейта")
	@app_commands.describe(image="Баннер к посту")

	async def look_for(self, ctx, image: discord.Attachment=None):
		await ctx.response.send_modal(LFInfo(self.bot, image))

	@look_for.error
	async def lf_error(self, ctx, error):
		await handle_errors(ctx, error, [])
	
	@commands.command(name="look-for",
		aliases=["lf","лук-фор","поиск-тимы","дщщл-ащк"],
		usage="`/look-for [изображение для баннера] <название игры> <описание>`",
		help="После введения этой команды у вас вылезет окно, куда вы можете вписать название для игры и подробное описание. После подтверждения ваш пост будет опубликован в канале `🔍・поиск-тимы`, где люди смогут присоединяться или отказываться от вашего созыва. В момент начала сбора людей для игры вы можете нажать на кнопку `Пингануть участников`, чтобы упомянуть всех, кто присоединился.\n###  Пример:\n`/look-for image.png\nмайнкрафт\nИщу тиммейта для игры на сервере\nАйпи сервера play.originrealms.com, только лицензия`")
	async def look_for_pointer(self, ctx):
		await ctx.reply(f"{Emojis.exclamation_mark} Используй **слэш** команду </look-for:1207711798732652555>", allowed_mentions=no_ping)


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
	
	@discord.ui.button(label="Присоединиться", emoji=Emojis.check, custom_id="look-for:join")
	async def join(self, ctx, button):
		await LookForView.response(ctx, "join")
	
	@discord.ui.button(label="Отказаться", emoji=Emojis.cross, custom_id="look-for:decline")
	async def decline(self, ctx: discord.Interaction, button: discord.ui.Button):
		await LookForView.response(ctx, "decline")
	
	@discord.ui.button(label="Пингануть участников", emoji=Emojis.users, custom_id="look-for:ping-all")
	async def ping_all(self, ctx: discord.Interaction, button: discord.ui.Button):
		joined_users = ctx.message.embeds[0].fields[1].value.replace("\n", " ")
		if ctx.user.id == db.find_one({"_id": ctx.message.id})["author_id"]:
			if "<@" in joined_users:
				await ctx.message.thread.send(f"{joined_users}, вас зовёт {ctx.user.mention}!")
				await ctx.response.send_message("Участники пингануты", ephemeral=True)
			else:
				await ctx.response.send_message(f"{Emojis.exclamation_mark} Пока нет кого пинговать", ephemeral=True)
		else:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являеетесь автором поста", ephemeral=True)


class LFInfo(discord.ui.Modal):
	def __init__(self, bot, image):
		super().__init__(title="Детали поста")
		self.custom_id="lf:details"
		self.bot = bot
		self.image = image

	game = discord.ui.TextInput(
		label="Игра",
		placeholder="майнкрафт",
		max_length=100
	)
	description = discord.ui.TextInput(
		label="Детали",
		style=discord.TextStyle.long,
		placeholder="Ищу тиммейта для игры на сервере\nАйпи сервера `play.originrealms.com`, только лицензия",
		max_length=1024
	)

	async def on_submit(self, ctx: discord.Interaction):
		embed = discord.Embed(title=f"{Emojis.spyglass} Ищу тиммейта для {self.game.value}", color=no_color)
		if not self.image:
			banners_count = {"minecraft": 3, "terraria": 0, "gartic": 0}
			games = {
				"minecraft": ["майнкрафт", "mc", "кубы", "говнокрафт"],
				"terraria": ["террария", "терка", "террка"],
				"gartic": ["гартик", "gartic phone", "сломанный телефон"]
			}
			validated_game = validate(self.game.value, games)
			if validated_game == None:
				game_banner = MISSING
			else:
				game_banner = discord.File(f"assets/game_banners/{validated_game}{randint(0, banners_count[validated_game])}.png",
				filename="banner.png")
				embed.set_image(url="attachment://banner.png")
		else:
			game_banner = await self.image.to_file(filename="banner.png")
			embed.set_image(url="attachment://banner.png")
		embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
		embed.add_field(name="Подробности", value=self.description.value, inline=False)
		embed.add_field(name=f"{Emojis.check} Присоединились", value="")
		embed.add_field(name=f"{Emojis.cross} Отклонили", value="")
		#
		LOOK_FOR_CHANNEL = await self.bot.fetch_channel(LOOK_FOR_CHANNEL_ID)
		lf_msg = await LOOK_FOR_CHANNEL.send(embed=embed, view=LookForView(), file=game_banner)
		db.insert_one({"_id": lf_msg.id, "author_id": ctx.user.id})
		await ctx.response.send_message(f"{Emojis.check} Пост создан: {lf_msg.jump_url}", ephemeral=True)
		await lf_msg.create_thread(name="Обсуждение")
	