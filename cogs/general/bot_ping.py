import discord
from discord.ext import commands

from utils.shortcuts import no_ping, no_color
from utils.msg_utils import Emojis

class BotPing(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	
	@commands.Cog.listener("on_message")
	async def main(self, msg):
		if msg.author == self.bot.user:
			return
		if msg.content.startswith("<@1196573758757028021>"):
			embed = discord.Embed(
				description=f"Привет! Я многофункциональный дискорд бот, созданный <@536441049644793858> и <@567014541507035148> и предназначенный чисто для этого сервера, с главной целью помочь вам в изучении команд, датапаков и ресурспаков, а также имею и другие интересные функции. Чтобы узнать больше о моих функциях, используйте команду </help:1270684227419246623>", 
				color=no_color)
			embed.set_author(name="AntBot", icon_url=self.bot.user.avatar.url)
			embed.set_thumbnail(url=self.bot.user.avatar.url)
			await msg.reply(embed=embed, view=BotPingView(), allowed_mentions=no_ping)

class BotPingView(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.add_item(discord.ui.Button(
			label="Исходный код",
			emoji=f"{Emojis.link}",
			url="https://github.com/FuncFusion/antbot"
		))
	