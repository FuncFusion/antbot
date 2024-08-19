import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import MISSING

from asyncio import sleep
from random import sample
from re import findall
from pymongo.mongo_client import MongoClient
from time import time
from typing import Literal

from settings import MONGO_URI, GIVEAWAYS_CHANNEL_ID, GIVEAWAYS_REQUESTS_CHANNEL_ID

from utils.general import handle_errors
from utils.msg_utils import Emojis, user_from_embed
from utils.shortcuts import no_color, no_ping
from utils.time import get_secs
from utils.users_db import DB as UDBUtils

users_db = MongoClient(MONGO_URI).antbot.users
db = MongoClient(MONGO_URI).antbot.giveaways

FOUR_WEEKS = 4 * 7 * 24 * 60 * 60


class GiveawayCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# Checking GAs from prev session
		self.check_giveaways.start()
	
	@tasks.loop(count=1, seconds=1)
	async def check_giveaways(self):
		for ga in db.find():
			await end_ga(ga["message_id"], self.bot)

	@app_commands.command(name="giveaway", description="Создаёт пост о розыгрыше в #🎉・розыгрыши.")
	async def ga(self, ctx, image: discord.Attachment=None):
		user_id = ctx.user.id
		if users_db.find_one({"_id": user_id}) == None:
			await UDBUtils.add_user(user_id, self.bot)
		user_doc = users_db.find_one({"_id": user_id})
		if user_doc["disapproved_ga"] <= 3 or int(time()) - user_doc["last_disapproved_ga"] > FOUR_WEEKS:
			await ctx.response.send_modal(GAInfo(self.bot, image))
		else:
			await ctx.response.send_message(f"{Emojis.cross} Слишком много отклонённых розыгрышей за последнее время")
	
	@commands.command(name="giveaway",
		aliases=["ga", "розыгрыш"],
		description="Создаёт пост о розыгрыше в канале `🎉・розыгрыши`.",
		usage="`/giveaway [изображение для баннера] <приз(ы)> <описание> <длительность> [количество победителей (по дефолту 1)] [доступ только по вайтлисту]`",
		help="После введения этой команды у вас вылезет окно, куда вы можете вписать все параметры розыгрыша (призы, описание, длительность, количество победителей, доступ только по вайтлисту, который настраивается командой </whitelist:1257432962081755168>). После подтверждения ваш розыгрыш будет оптравлен на проверку модерации. Если она одобрит ваш розыгрыш, он будет опубликован в канале `🎉・розыгрыши`. Вы также можете настраивать, кто НЕ может учавствовать в ваших розыгрышах с помощью команды </blacklist:1257067280643129444>.\n### Пример:\n`/giveaway` `Ключ к Minecraft Dungeons` `Учтите, что игра не для слабых пк, так что если вы не собираетесь играть со мной в эту игру, НЕ учавствуйте в конкурсе!` `1день 5ч`")
	async def giveaway_pointer(self, ctx):
		await ctx.reply(f"{Emojis.exclamation_mark} Используй **слэш** команду </giveaway:1255859084792430732>", allowed_mentions=no_ping)

class GAInfo(discord.ui.Modal):
	def __init__(self, bot, image):
		super().__init__(title="Детали розыгрыша")
		self.custom_id="ga:details"
		self.bot = bot
		self.image = image

	prize = discord.ui.TextInput(
		label="Приз(ы)",
		style=discord.TextStyle.long,
		min_length=3,
		max_length=1999
	)
	description = discord.ui.TextInput(
		label="Описание",
		style=discord.TextStyle.long,
		min_length=5,
		max_length=1999
	)
	end_date = discord.ui.TextInput(
		label="Закончится через...",
		placeholder="10 минут 15 секнуд/2 дня/15ч 18 мин",
		min_length=2
	)
	winners_count = discord.ui.TextInput(
		label="Количество победителей",
		default="1"
	)
	whitelist_only = discord.ui.TextInput(
		label="Доступ по вайтлисту",
		placeholder="1/Да/True/T/эщкере",
		required=False
	)

	async def on_submit(self, ctx: discord.Interaction):
		end_date_secs = get_secs(self.end_date.value)
		if end_date_secs < 60:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Неправильно указано время.", ephemeral=True)
			return
		#
		embed = discord.Embed(color=no_color)
		embed.add_field(name=f"{Emojis.party_popper} Приз(ы)", value=self.prize.value)
		embed.add_field(name="Описание", value=self.description.value, inline=False)
		embed.add_field(name="Конкурс закончится", value=f"<t:{int(time()) + end_date_secs}:R>", inline=False)
		embed.set_author(name=ctx.user.name, icon_url=ctx.user.display_avatar.url)
		#img
		if self.image != None:
			image_attachment = await self.image.to_file(filename=self.image.filename)
		else:
			image_attachment = MISSING
		embed.set_image(url=f"attachment://{self.image.filename}")
		#
		ga_judge_channel = await self.bot.fetch_channel(GIVEAWAYS_REQUESTS_CHANNEL_ID)
		ga_msg = await ga_judge_channel.send(embed=embed, file=image_attachment, view=JudgeGA(self.bot))
		ga_doc = {
			"_id": ga_msg.id,
			"author_id": ctx.user.id,
			"end_date": end_date_secs,
			"winners_count": max(1, int(self.winners_count.value)),
			"participants": [],
			"blacklist": []
		}
		if bool(self.whitelist_only.value):
			ga_doc.update({"whitelist": []})
		db.insert_one(ga_doc)
		await ctx.response.send_message(f"{Emojis.check} Розыгрыш отправлен на проверку", ephemeral=True)

	
class JudgeGA(discord.ui.View):
	def __init__(self, bot, verdict=None):
		super().__init__(timeout=None)
		self.bot = bot
		if verdict != None:
			self.approve.disabled = True
			self.disapprove.disabled = True
			if verdict == "approved":
				self.approve.style = discord.ButtonStyle.blurple
			else:
				self.disapprove.style = discord.ButtonStyle.blurple
	
	@discord.ui.button(label="Одобрить", emoji=Emojis.check, custom_id="ga:approve")
	async def approve(self, ctx, button):
		ga_author = await self.bot.fetch_user(db.find_one({"_id":ctx.message.id})["author_id"])
		ga_channel = await self.bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
		posted_ga = await ga_channel.send(embed=ctx.message.embeds[0], view=TakePart())
		await posted_ga.create_thread(name=f"Розыгрыш {ga_author.name}")
		db.update_one({"_id":ctx.message.id}, {"$set": {"message_id": posted_ga.id}})
		await ctx.response.edit_message(view=JudgeGA(self.bot, "approved"))
		await ga_author.send(f"{Emojis.check} Ваш розыгрыш одобрен {posted_ga.jump_url}")
		await end_ga(posted_ga.id, self.bot)

	@discord.ui.button(label="Отклонить", emoji=Emojis.cross, custom_id="ga:disapprove")
	async def disapprove(self, ctx, button):
		user_id = db.find_one({"_id":ctx.message.id})["author_id"]
		users_db.update_one({"_id": user_id}, {"$inc": {"disapproved_ga": 1}})
		users_db.update_one({"_id": user_id}, {"$set": {"last_disapproved_ga": int(time())}})
		db.delete_one({"_id": ctx.message.id})
		await ctx.response.edit_message(view=JudgeGA(self.bot, "disapproved"))
		ga_author = await self.bot.fetch_user(user_from_embed(ctx.message))
		await ga_author.send(f"{Emojis.cross} Ваш розыгрыш отклонён")

class TakePart(discord.ui.View):
	def __init__(self, particicpants_count="0", disable=False):
		super().__init__(timeout=None)
		self.take_part.label = particicpants_count
		if disable:
			self.take_part.disabled = True
	
	@discord.ui.button(emoji=Emojis.party_popper, custom_id="ga:take-part")
	async def take_part(self, ctx, button):
		ga = db.find_one({"message_id":ctx.message.id})
		if ctx.user.id in ga["participants"]:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы уже учавствуете в конкурсе", ephemeral=True)
		elif ctx.user.id in ga["blacklist"]:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы в блэклисте", ephemeral=True)
		elif "whitelist" in ga and ctx.user.id not in ga["whitelist"]:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не в вайтлисте", ephemeral=True)
		else:
			db.update_one({"message_id": ctx.message.id}, {"$push": {"participants": ctx.user.id}})
			await ctx.message.edit(view=TakePart(str(int(self.take_part.label)+1)))
			await ctx.response.send_message(f"{Emojis.check} Вы добавлены в список учасвствующих", ephemeral=True)


async def end_ga(msg_id, bot):
	ga_channel = await bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
	msg = await ga_channel.fetch_message(msg_id)
	end_date = msg.embeds[0].fields[2].value[3:-3]
	await sleep(int(end_date) - int(time()))
	#
	ga = db.find_one({"message_id": msg_id})
	participants_count = len(ga["participants"])
	winners_count = ga["winners_count"] if ga["winners_count"] <= participants_count else participants_count
	winners = sample(ga["participants"], winners_count)
	if len(winners) == 1:
		edited_embed = msg.embeds[0].insert_field_at(1, name=f"{Emojis.trophy} Победитель",
		value=f"<@{winners[0]}>")
	else:
		edited_embed = msg.embeds[0].insert_field_at(1, name=f"{Emojis.trophy} Победители",
		value="\n".join([f"{i}. <@{winners[i]}>" for i in range(len(winners))]))
	await msg.edit(embed=edited_embed, view=TakePart(participants_count, True))
	await msg.thread.send(f"# {edited_embed.fields[1].name}\n{edited_embed.fields[1].value}")
	db.delete_one({"message_id": msg_id})


class GAModerationCommands(commands.Cog):

	@commands.hybrid_command(
		aliases=["bl", "бл", "чс"],
		description="Оперирует блэклистом розыгрыша.",
		usage="`/blacklist <add|remove> <пользователь(и)>`",
		help="Команда должна быть отправлена в ветку розыгрыша его автором. При добавлении пользователя в блэклист он также исключается из списка участников.\n### Пример:\n`/blacklist add <@808665387142873108>`\n`/blacklist remove <@808665387142873108> <@511049889371783180>`")
	@app_commands.describe(users="@Упоминания пользователей")
	async def blacklist(self, ctx, operation: Literal["add", "remove"], users: str):
		if not (isinstance(ctx.channel, discord.Thread) and ctx.channel.parent.id == GIVEAWAYS_CHANNEL_ID):
			raise Exception("AttributeError")
		user_ids = list(map(int, findall(r"(?<=<@)\d+(?=>)", users)))
		if len(user_ids) == 0:
			raise commands.UserNotFound("No users found")
		ga_filter = {"message_id": ctx.channel.id}
		ga = db.find_one(ga_filter)
		if operation == "add":
			for id in user_ids:
				db.update_one(ga_filter, {"$push": {"blacklist": id}})
				db.update_one(ga_filter, {"$pull": {"participants": id}})
			ga = db.find_one(ga_filter)
			starter_message = await ctx.channel.parent.fetch_message(ctx.channel.id)
			await starter_message.edit(view=TakePart(str(len(ga["participants"]))))
			await ctx.reply(f"{Emojis.check} {users} Добален{'ы' if users.count('@') > 1 else ''} в блэклист", allowed_mentions=no_ping)
		elif operation == "remove":
			for id in user_ids:
				db.update_one(ga_filter, {"$pull": {"blacklist": id}})
			await ctx.reply(f"{Emojis.check} {users} Убран{'ы' if users.count('@') > 1 else ''} с блэклиста", allowed_mentions=no_ping)
	@blacklist.error
	async def bl_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.BadLiteralArgument,
				"msg": "Неверная сабкоманда"
			},
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов"
			},
			{
				"exception": commands.UserNotFound,
				"msg": "Не найдено ни одного пользователя из списка"
			},
			{
				"contains": "AttributeError",
				"msg": "Это не ветка розыгрыша"
			},
			{
				"contains": "NoneType",
				"msg": "Это не ветка розыгрыша"
			}
		])

	@commands.hybrid_command(
		aliases=["wl", "вл", "бс"],
		description="Оперирует вайтлистом розыгрыша.",
		usage="`/whitelist <add|remove> <пользователь(и)>`",
		help="Работает так же, как и </blacklist:1257067280643129444>, но позволяет манипулировать **вайт**листом розыгрыша.")
	@app_commands.describe(users="@Упоминания пользователей")
	async def whitelist(self, ctx, operation: Literal["add", "remove"], users: str):
		if not (isinstance(ctx.channel, discord.Thread) and ctx.channel.parent.id == GIVEAWAYS_CHANNEL_ID):
			raise Exception("AttributeError")
		user_ids = list(map(int, findall(r"(?<=<@)\d+(?=>)", users)))
		if len(user_ids) == 0:
			raise commands.UserNotFound("No users found")
		ga_filter = {"message_id": ctx.channel.id}
		ga = db.find_one(ga_filter)
		if operation == "add":
			for id in user_ids:
				db.update_one(ga_filter, {"$push": {"whitelist": id}})
			await ctx.reply(f"{Emojis.check} {users} Добален{'ы' if users.count('@') > 1 else ''} в вайтлист", allowed_mentions=no_ping)
		elif operation == "remove":
			for id in user_ids:
				db.update_one(ga_filter, {"$pull": {"whitelist": id}})
				db.update_one(ga_filter, {"$pull": {"participants": id}})
			ga = db.find_one(ga_filter)
			starter_message = await ctx.channel.parent.fetch_message(ctx.channel.id)
			await starter_message.edit(view=TakePart(str(len(ga["participants"]))))
			await ctx.reply(f"{Emojis.check} {users} Убран{'ы' if users.count('@') > 1 else ''} с вайтлиста", allowed_mentions=no_ping)
	@whitelist.error
	async def wl_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.BadLiteralArgument,
				"msg": f"Неверная сабкоманда"
			},
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"Не хватает аргументов"
			},
			{
				"exception": commands.UserNotFound,
				"msg": "Не найдено ни одного пользователя из списка"
			},
			{
				"contains": "AttributeError",
				"msg": f"Это не ветка розыгрыша"
			},
			{
				"contains": "NoneType",
				"msg": f"Это не ветка розыгрыша"
			}
		])
