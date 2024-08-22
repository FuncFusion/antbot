import discord
from discord.ext import commands

from utils.shortcuts import no_ping, no_color

class BotPing(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener("on_message")
	async def main(self, msg):
		if msg.author == self.bot.user:
			return
		if msg.content == ("<@1196573758757028021>"):
			thumbnail = discord.File("assets/antbot.png", filename="antbot.png")
			embed = discord.Embed(title="Привет!", description=f"Я многофункциональный дискорд бот, созданный <@536441049644793858> и <@567014541507035148> и предназначенный чисто для этого сервера, с главной целью помочь вам в изучении команд, датапаков и ресурспаков, а также имею и другие интересные функции. Используйте команду </help:1270684227419246623>, чтобы узнать больше о моих функциях.", color=no_color)
			embed.set_thumbnail(url="attachment://antbot.png")
			await msg.reply(embed=embed, file=thumbnail, allowed_mentions=no_ping)
			