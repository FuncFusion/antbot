import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from pymongo.mongo_client import MongoClient

from settings import MONGO_URI, GIVEAWAYS_CHANNEL_ID, GIVEAWAYS_REQUESTS_CHANNEL_ID

from utils.shortcuts import no_color
from utils.msg_utils import Emojis

db = MongoClient(MONGO_URI).antbot.giveaways


class GiveawayCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(name="giveaway", aliases=[ "гивевей", "гивэвей", "гивэвэй", "розыгрышь", "розыграть"],
		description="Создаёт пост о розыграше в #🎉・розыгрыши")
	async def ga(self, ctx, image: discord.Attachment=None):
		await ctx.send_modal(GAInfo(self.bot, image))
	

class GAInfo(discord.ui.Modal):
	def __init__(self, bot, image):
		super().__init__(title="Детали розыграша")
		self.custom_id="ga:details"
		self.bot = bot
		self.image = image

	title = discord.ui.TextInput(
		label="Приз (Заголовок)",
		placeholder="",
		max_length=123
	)
	condition = discord.ui.TextInput(
		label="Условие",
		style=discord.TextStyle.long,
		placeholder="",
		max_length=1999
	)

	async def on_submit(self, ctx: discord.Interaction):
		embed = discord.Embed(description=f"# {self.title}\n{self.condition}", color=no_color)
		embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
		if self.image != None:
			image = await self.image.to_file()
		else:
			image = MISSING
		image_file = discord.File(image, filename="giveaway.png")
		embed.set_image(url="attachment://giveaway.png")
		ga_chnl = await self.bot.fetch_channel(GIVEAWAYS_REQUESTS_CHANNEL_ID)
		ga_msg = await ga_chnl.send(embed=embed, file=image_file)
		db.insert_one({
			"_id": ga_msg.id,
			"participants": []
		})
		await ctx.response.send_message( ephemeral=True)

	
class JudgeGA(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Одобрить", emoji=Emojis.check, custom_id="ga:approve")
	async def approve(self, ctx, button):
		ga_channel = await self.bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
		posted_ga = await ga_channel.send(embed=ctx.message.embed)
		db.update_one({"_id":str(ctx.message.id)}, {"$set": {"_id": str(posted_ga.id)}})

	@discord.ui.button(label="Отклонить", emoji=Emojis.cross, custom_id="ga:disapprove")
	async def disapprove(self, ctx, button):
		pass

class TakePart(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Принять участие", emoji=Emojis.check, custom_id="ga:take-part")
	async def take_part(self, ctx, button):
		db.update_one({"_id":str(ctx.message.id)}, {"$push": {"participants": ctx.author.id}})
		await ctx.response.send_message(f"{Emojis.check} Вы добавлены в список уасвствующих", ephemeral=True)


