import discord
from discord import ui
from discord.ext import commands

from utils import no_ping, Emojis, LazyLayout

class BotPing(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	
	@commands.Cog.listener("on_message")
	async def main(self, msg):
		if msg.author == self.bot.user:
			return
		if msg.content == ("<@1196573758757028021>"):
			await msg.reply(
				view=LazyLayout(
					ui.Section(
						"Привет! Я многофункциональный дискорд бот, созданный <@536441049644793858> "
						"и <@567014541507035148> и предназначенный чисто для этого сервера Anthill. "
						"Моя главная цель — помочь вам в изучении команд, датапаков и ресурспаков, "
						"но я также имею и другие интересные функции. Используйте команду "
						"</help:1270684227419246623>, чтобы узнать больше о моих функциях.",
						accessory=ui.Thumbnail(self.bot.user.avatar.url) 
					),
					ui.Separator(),
					ui.ActionRow(
						ui.Button(
							label="Исходный код",
							emoji=f"{Emojis.github}",
							url="https://github.com/FuncFusion/antbot"
						),
						ui.Button(
							label="Предложить идею/зарепортить баг",
							emoji=f"{Emojis.edited_msg}",
							url="https://discord.com/channels/914772142300749854/1276169141572730880"
						)
					)
				), 
				allowed_mentions=no_ping
			)
