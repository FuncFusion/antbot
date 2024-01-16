import discord
from discord.ext import commands
from discord import app_commands


class GeneralCommands(commands.Cog):
	def __init__(self, bot):
		@bot.tree.command(name="сказать", description="Отправить от лица Антобота")
		@app_commands.describe(text="Текст, который будет отправлен ботом")
		async def say(interaction: discord.Interaction, text: str):
			await interaction.response.send_message(text)
