import discord
from discord.ext import commands
from discord import app_commands

help_forum_id = 1169322456125800498
links = {
	"pinned_help": "https://discord.com/channels/914772142300749854/1021488153909018704"
}

class HelpCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["thx", "ерфтлы", "ерч", "спасибо", "спс", "благодраю", "благодарен"]) 
		@app_commands.describe(helper="Человек, который помго вам решить проблему")
		async def thanks(ctx, helper: discord.Message=None):
			
			await ctx.sendd(embed=embed)

		@bot.hybrid_command(aliases=["solve", "ыщдму", "куыщдму", "решено"]) 
		@app_commands.describe(solution="Сообщение которое помогло решить проблему")
		async def resolve(ctx, solution: discord.Message=None):
			# Error handling
			if type(ctx.channel) != discord.threads.Thread and ctx.channel.parent_id != help_forum_id:
				await ctx.send("Эта команда работает только в ветках помощи")
			elif ctx.author == ctx.channel.owner or ctx.author.resolved_permissions.manage_messages:
				await ctx.send("Вы не являетесь автором этой ветки либо модератором")
			elif solution != None:
				await ctx.send("Пожалуйста, укажите сообщение которое помогло с решением вашей \
				проблемы, ответив, либо указав ссылку на него".replace("\t", ""))
			else:
				# Building embed
				embed = discord.Embed(title="✅ Проблема решена", color=discord.Color.dark_embed(),
					description=f"Решение: {solution.jump_url}")
				await ctx.send(embed=embed)

class HelpListeners(commands.Cog):
	def __init__(self, bot):
	
		@bot.listen("on_thread_create")
		async def help_in_chat(trd):
			if trd.parent_id == help_forum_id:
				# Building embed
				embed = discord.Embed(title="📌 Ознакомся с правилами", color=discord.Color.dark_embed(), 
					description=f"Если ещё не читал, прочти в закрепе ({links['pinned_help']}) рекомендации \
					к веткам помощи, и о том, как работают некоторые её аспекты. Следование всем рекомендациям \
					поможет тебе получить как можно более эффективную помощь.".replace("\t", ""))
				#
				await trd.send(embed=embed)