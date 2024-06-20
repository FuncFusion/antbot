import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

from pymongo.mongo_client import MongoClient

from settings import MONGO_URI, GIVEAWAYS_CHANNEL_ID

from  utils.shortcuts import no_color

db = MongoClient(MONGO_URI).antbot.giveaways


class GiveawayCommand(commands.Cog):
	def __init__(self):
		pass

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
		label="Приз",
		style=discord.TextStyle.long,
		placeholder="",
		max_length=1999
	)

	async def on_submit(self, ctx: discord.Interaction):
		embed = discord.Embed(description=f"# {self.title}\n{self.condition}", color=no_color)
		ga_chnl = await self.bot.fetch_channel(GIVEAWAYS_CHANNEL_ID)
		if self.image != None:
			image = await self.image.to_file()
		else:
			image = MISSING
		ga_msg = await ga_chnl.send(embed=embed)
		db.insert_one({
			"_id": ga_msg.id,
			"participants": []
		})
		await ctx.response.send_message( ephemeral=True)
