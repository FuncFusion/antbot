import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from time import time
from pymongo.mongo_client import MongoClient

from settings import MONGO_URI, GIVEAWAYS_CHANNEL_ID, GIVEAWAYS_REQUESTS_CHANNEL_ID

from utils.shortcuts import no_color
from utils.msg_utils import Emojis
from utils.users_db import DB as UDBUtils

users_db = MongoClient(MONGO_URI).antbot.users
db = MongoClient(MONGO_URI).antbot.giveaways

FOUR_WEEKS = 4 * 7 * 24 * 60 * 60


class GiveawayCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="giveaway", description="Создаёт пост о розыграше в #🎉・розыгрыши")
	async def ga(self, ctx, image: discord.Attachment=None):
		user_id = str(ctx.user.id)
		if users_db.find_one({"_id": user_id}) == None:
			await UDBUtils.add_user(user_id, self.bot)
		user_doc = users_db.find_one({"_id": user_id})
		if user_doc["disapproved_ga"] <= 3 or user_doc["last_disapproved_ga"] - int(time()) > FOUR_WEEKS:
			await ctx.response.send_modal(GAInfo(self.bot, image))
		else:
			await ctx.response.send_message(f"{Emojis.cross} Динаху")
	

class GAInfo(discord.ui.Modal):
	def __init__(self, bot, image):
		super().__init__(title="Детали розыграша")
		self.custom_id="ga:details"
		self.bot = bot
		self.image = image

	prize = discord.ui.TextInput(
		label="Приз (Заголовок)",
		max_length=123
	)
	condition = discord.ui.TextInput(
		label="Условие",
		style=discord.TextStyle.long,
		max_length=1999
	)

	async def on_submit(self, ctx: discord.Interaction):
		embed = discord.Embed(description=f"# {self.prize}\n{self.condition}", color=no_color)
		embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
		if self.image != None:
			image_attachment = await self.image.to_file(filename="giveaway.png")
		else:
			image_attachment = MISSING
		embed.set_image(url="attachment://giveaway.png")
		ga_judge_channel = await self.bot.fetch_channel(GIVEAWAYS_REQUESTS_CHANNEL_ID)
		ga_msg = await ga_judge_channel.send(embed=embed, file=image_attachment, view=JudgeGA(self.bot))
		db.insert_one({
			"_id": ga_msg.id,
			"participants": []
		})
		await ctx.response.send_message( ephemeral=True)

	
class JudgeGA(discord.ui.View):
	def __init__(self, bot, disable=False):
		super().__init__(timeout=None)
		self.bot = bot
		if disable:
			self.approve.disabled = True
			self.disapprove.disabled = True
	
	@discord.ui.button(label="Одобрить", emoji=Emojis.check, custom_id="ga:approve")
	async def approve(self, ctx, button):
		ga_channel = await self.bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
		posted_ga = await ga_channel.send(embed=ctx.message.embeds[0])
		db.update_one({"_id":str(ctx.message.id)}, {"$set": {"_id": str(posted_ga.id)}})
		await ctx.response.edit_message(view=JudgeGA(self.bot, True))
		await ctx.user.send(f"{Emojis.check} Ваш розыгрыш одобрен")

	@discord.ui.button(label="Отклонить", emoji=Emojis.cross, custom_id="ga:disapprove")
	async def disapprove(self, ctx, button):
		user_id = ctx.message.embeds[0].author.icon_url.split("/")[4]
		users_db.update_one({"_id": str(user_id)}, {"$inc": {"disapproved_ga": 1}})
		users_db.update_one({"_id": str(user_id)}, {"$set": {"last_disapproved_ga": int(time())}})
		await ctx.response.edit_message(view=JudgeGA(self.bot, True))
		await ctx.user.send(f"{Emojis.cross} Ваш розыгрыш отклонён")

class TakePart(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Принять участие", emoji=Emojis.check, custom_id="ga:take-part")
	async def take_part(self, ctx, button):
		db.update_one({"_id":str(ctx.message.id)}, {"$push": {"participants": ctx.author.id}})
		await ctx.response.send_message(f"{Emojis.check} Вы добавлены в список уасвствующих", ephemeral=True)


