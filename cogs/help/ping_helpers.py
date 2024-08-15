import discord
from discord.ext import commands, tasks
from discord.utils import MISSING

from asyncio import sleep
from time import time
from pymongo.mongo_client import MongoClient

from settings import HELP_FORUM_ID, MONGO_URI, DATAPACKS_TAG, RESOURCEPACKS_TAGS, DATAPACK_MASTER_ROLE, \
	RESOURCEPACK_MASTER_ROLE
from utils.msg_utils import Emojis
from utils.shortcuts import  no_color

db = MongoClient(MONGO_URI).antbot.not_offered_help_threads

DAY = 1


class PingHelpers(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.check_threads.start()
	
	@tasks.loop(seconds=1, count=1)
	async def check_threads(self):
		for trd_doc in db.find():
			trd = await self.bot.fetch_channel(trd_doc["_id"])
			await self.offer_ping_helpers(trd_doc["about_dp"], trd_doc["about_rp"], trd, trd_doc["when_offer"])

	async def offer_ping_helpers(self, about_dp, about_rp, trd, when_offer):
		try:
			db.insert_one({
				"_id": trd.id,
				"about_dp": about_dp,
				"about_rp": about_rp,
				"when_offer": when_offer
			})
		except:pass
		left_before_offer = when_offer - int(time())
		await sleep(left_before_offer)
		trd = await self.bot.fetch_channel(trd.id)
		if not trd.archived:
			await trd.send(f"{trd.owner.mention}, не получили ответ? Можете позвать мастеров на помощь!", 
				view=Ping_related_helpers(about_dp, about_rp))
		db.delete_one({"_id": trd.id})

	@commands.Cog.listener("on_thread_create")
	async def new_help_post(self, trd):
		await sleep(0.5)
		if trd.parent_id == HELP_FORUM_ID:
			about_dp = about_rp = False
			if DATAPACKS_TAG in trd.applied_tags:
				about_dp = True
			if any((tag in trd.applied_tags for tag in RESOURCEPACKS_TAGS)):
				about_rp = True
			if not (about_dp and about_rp):
				pass
			await self.offer_ping_helpers(about_dp, about_rp, trd, int(time())+DAY)


class Ping_related_helpers(discord.ui.View):
	def __init__(self, about_dp=True, about_rp=False, disabled=False):
		super().__init__(timeout=None)
		self.about_dp = about_dp
		self.about_rp = about_rp
		if disabled:
			self.ping_dp_masters.disabled = True
			self.ping_rp_masters.disabled = True
			self.ping_all_masters.disabled = True
		if (about_dp and about_rp):
			self.remove_item(self.ping_dp_masters)
			self.remove_item(self.ping_rp_masters)
		else:
			self.remove_item(self.ping_all_masters)
			if not about_dp:
				self.remove_item(self.ping_dp_masters)
			elif not about_rp:
				self.remove_item(self.ping_rp_masters)
	
	async def buttons_callback(self, ctx, mentions):
		is_owner = True if ctx.user == ctx.channel.owner else False
		if is_owner:
			await ctx.response.send_message(mentions)
			await ctx.message.edit(view=Ping_related_helpers(self.about_dp, self.about_rp, True))
		else:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являетесь автором поста", ephemeral=True)

	@discord.ui.button(label="Пингануть датапак мастеров", emoji=Emojis.deta_rack, custom_id="starter_message:ping_dp")
	async def ping_dp_masters(self, ctx: discord.Interaction, button: discord.ui.Button):
		await self.buttons_callback(ctx, f"<@&{DATAPACK_MASTER_ROLE}>")

	@discord.ui.button(label="Пингануть ресурспак мастеров", emoji=Emojis.resource_rack, custom_id="starter_message:ping_rp")
	async def ping_rp_masters(self, ctx: discord.Interaction, button: discord.ui.Button):
		await self.buttons_callback(ctx, f"<@&{RESOURCEPACK_MASTER_ROLE}>")
	
	@discord.ui.button(label="Пингануть всех мастеров", emoji=Emojis.deta_rack, custom_id="starter_message:ping_all")
	async def ping_all_masters(self, ctx: discord.Interaction, button: discord.ui.Button):
		await self.buttons_callback(ctx, f"<@&{DATAPACK_MASTER_ROLE}> <@&{RESOURCEPACK_MASTER_ROLE}>")
