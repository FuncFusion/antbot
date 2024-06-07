import discord
from discord.ext import commands

from utils.shortcuts import no_color, no_ping


class PingCommand(commands.Cog):
	@commands.hybrid_command(aliases=["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"], 
		description="Показывает пинг бота.")
	async def ping(self, ctx):
		embed = discord.Embed(title="🏓 Понг!", color=no_color)
		embed.add_field(name=f'Мой пинг: {round(self.bot.latency*1000)}ms', value="", inline=True)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
