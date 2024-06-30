import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from asyncio import sleep
from random import sample
from time import time
from typing import Literal
from pymongo.mongo_client import MongoClient

from settings import MONGO_URI, GIVEAWAYS_CHANNEL_ID, GIVEAWAYS_REQUESTS_CHANNEL_ID

from utils.time import get_secs
from utils.shortcuts import no_color
from utils.msg_utils import Emojis
from utils.users_db import DB as UDBUtils

users_db = MongoClient(MONGO_URI).antbot.users
db = MongoClient(MONGO_URI).antbot.giveaways

FOUR_WEEKS = 4 * 7 * 24 * 60 * 60

def from_embed(message):
	return int(message.embeds[0].author.icon_url.split("/")[4])


class GiveawayCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="giveaway", description="Создаёт пост о розыграше в #🎉・розыгрыши")
	async def ga(self, ctx, image: discord.Attachment=None):
		user_id = ctx.user.id
		if users_db.find_one({"_id": user_id}) == None:
			await UDBUtils.add_user(user_id, self.bot)
		user_doc = users_db.find_one({"_id": user_id})
		if user_doc["disapproved_ga"] <= 3 or int(time()) - user_doc["last_disapproved_ga"] > FOUR_WEEKS:
			await ctx.response.send_modal(GAInfo(self.bot, image))
		else:
			await ctx.response.send_message(f"{Emojis.cross} Слишком много отклонённых розыграшей за последнее время")
	

class GAInfo(discord.ui.Modal):
	def __init__(self, bot, image):
		super().__init__(title="Детали розыграша")
		self.custom_id="ga:details"
		self.bot = bot
		self.image = image

	prize = discord.ui.TextInput(
		label="Приз(ы)",
		style=discord.TextStyle.long,
		max_length=1999
	)
	description = discord.ui.TextInput(
		label="Описание",
		style=discord.TextStyle.long,
		max_length=1999
	)
	end_date = discord.ui.TextInput(
		label="Закончится через...",
		placeholder="10 минут 15 секнуд/2 дня/15ч 18 мин"
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
		embed = discord.Embed(color=no_color)
		embed.add_field(name=f"{Emojis.party_popper} Приз(ы)", value=self.prize.value)
		embed.add_field(name="Описание", value=self.description.value, inline=False)
		embed.add_field(name="Конкурс закончится", value=f"<t:{int(time()) + get_secs(self.end_date.value)}:R>", inline=False)
		embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
		#img
		if self.image != None:
			image_attachment = await self.image.to_file(filename="giveaway.png")
		else:
			image_attachment = MISSING
		embed.set_image(url="attachment://giveaway.png")
		#
		ga_judge_channel = await self.bot.fetch_channel(GIVEAWAYS_REQUESTS_CHANNEL_ID)
		ga_msg = await ga_judge_channel.send(embed=embed, file=image_attachment, view=JudgeGA(self.bot))
		db.insert_one({
			"_id": ga_msg.id,
			"winners_count": int(self.winners_count.value),
			"participants": [],
			"blacklist": []
		})
		await ctx.response.send_message(f"{Emojis.check} Розыгрыш отправлен на проверку", ephemeral=True)

	
class JudgeGA(discord.ui.View):
	def __init__(self, bot, disable=False):
		super().__init__(timeout=None)
		self.bot = bot
		if disable:
			self.approve.disabled = True
			self.disapprove.disabled = True
	
	@discord.ui.button(label="Одобрить", emoji=Emojis.check, custom_id="ga:approve")
	async def approve(self, ctx, button):
		ga_author = await self.bot.fetch_user(from_embed(ctx.message))
		ga_channel = await self.bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
		posted_ga = await ga_channel.send(embed=ctx.message.embeds[0], view=TakePart())
		await posted_ga.create_thread(name=f"Розыгрыш {ga_author.name}")
		db.update_one({"_id":ctx.message.id}, {"$set": {"message_id": posted_ga.id}})
		await ctx.response.edit_message(view=JudgeGA(self.bot, True))
		await ga_author.send(f"{Emojis.check} Ваш розыгрыш одобрен")
		await end_ga(posted_ga)

	@discord.ui.button(label="Отклонить", emoji=Emojis.cross, custom_id="ga:disapprove")
	async def disapprove(self, ctx, button):
		user_id = from_embed(ctx.message)
		users_db.update_one({"_id": user_id}, {"$inc": {"disapproved_ga": 1}})
		users_db.update_one({"_id": user_id}, {"$set": {"last_disapproved_ga": int(time())}})
		db.delete_one({"_id": ctx.message.id})
		await ctx.response.edit_message(view=JudgeGA(self.bot, True))
		ga_author = await self.bot.fetch_user(from_embed(ctx.message))
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

async def end_ga(msg: discord.Message):
	end_date = msg.embeds[0].fields[2].value[3:-3]
	await sleep(int(end_date) - int(time()))
	#
	ga = db.find_one({"message_id": msg.id})
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

class GAModerationCommands(commands.Cog):

	@commands.hybrid_command(name="blacklist", aliases=["бл", "чс"])
	async def bl(self, ctx, operation:str, users: discord.User):
		await ctx.send("Hello, basement!")
