import discord
from discord.ext import commands

from utils import LazyLayout, no_ping


class PingCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"], 
		description="Показывает пинг бота.",
		usage="`/ping`",
		help="")
	async def ping(self, ctx):
		await ctx.reply(view=LazyLayout(
			discord.ui.TextDisplay(
				"# 🏓 Понг!\n"
				f"**Мой пинг: {round(self.bot.latency*1000)}ms**"
			)), 
			allowed_mentions=no_ping
		)
