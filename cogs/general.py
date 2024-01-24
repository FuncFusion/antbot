import discord
from discord.ext import commands
from discord import app_commands


class GeneralCommands(commands.Cog):
	def __init__(self, bot):
		
		@bot.hybrid_command(aliases=["сказать", "молвить"],
					  description="Сказать от имени бота")
		@app_commands.describe(text="Текст сообщения, которое отправит бот")
		async def say(ctx, *, text: str):
			temp = await ctx.send("_ _")
			await ctx.channel.send(text)
			await temp.delete()
			await ctx.message.delete()
