import discord
from discord.ext import commands
from discord import app_commands


class GeneralCommands(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(name="server-info", aliases=["info", "штащ","сервер-инфо", "инфо"],
					  description="Показывает инфу о сервере")
		async def server_info(ctx):
			# setup vars
			server = ctx.guild
			member_count = 0
			bot_count = 0
			for member in server.members:
				if member.bot:
					bot_count += 1
				else:
					member_count += 1
			invitation_link = await ctx.channel.create_invite(max_age=86400)
			# Building embed
			embed = discord.Embed(title=server.name, color=server.owner.roles[-1].color.value)
			embed.set_thumbnail(url=server.icon.url)
			embed.add_field(name="Владелец", value=f"👑 <@{server.owner_id}>", inline=False)
			embed.add_field(name="Сервер создан", value=f"📅 <t:{int(server.created_at.timestamp())}>", inline=False)
			embed.add_field(name="Участники", value=f"👤 {member_count} • 🤖 {bot_count}", inline=False)
			embed.add_field(name="Каналы", value=f"⌨ {len(server.text_channels)} • 🔊 {len(server.voice_channels)} • 💬 {len(server.forums)}", inline=False)
			embed.add_field(name="Роли", value=f"🎭 {len(server.roles)}", inline=False)
			embed.add_field(name="Приглашение (иссякает через сутки)", value=f"🔗 {invitation_link}")
			embed.set_footer(text=f"🆔 {server.id}")
			await ctx.send(embed=embed)
		
		@bot.hybrid_command(aliases=["сказать", "молвить"],
					  description="Сказать от имени бота")
		@app_commands.describe(text="Текст сообщения, которое отправит бот")
		async def say(ctx, *, text: str):
			temp = await ctx.send("_ _", ephemeral=True)
			await ctx.channel.send(text)
			await temp.delete()
			await ctx.message.delete()
