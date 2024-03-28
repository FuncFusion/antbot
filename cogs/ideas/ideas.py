import discord
from discord.ext import commands
from discord import app_commands

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from settings import IDEAS_CHANNEL_ID
from settings import MONGO_URI
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color

from json import load, dump

db = MongoClient(MONGO_URI, server_api=ServerApi('1')).antbot.ideas

class IdeaView(discord.ui.View):
	def __init__(self, votes=["0", "0"]):
		super().__init__(timeout=None)
		# Setting up variables
		self.upvote.label = votes[0]
		self.downvote.label = votes[1]

	@discord.ui.button(label="0", emoji=Emojis.check, style=discord.ButtonStyle.grey, custom_id="ideas:upvote")
	async def upvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		# Setting up variables
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "up")
		idea = Ideas.get(idea_num)
		upvoters = str(len(idea["upvoters"]))
		downvoters = str(len(idea["downvoters"]))
		# Chnaging votes
		await ctx.response.edit_message(view=IdeaView(votes=[upvoters, downvoters]))
	
	@discord.ui.button(label="0", emoji=Emojis.cross, style=discord.ButtonStyle.grey, custom_id="ideas:downvote")
	async def downvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		# Setting up variables
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "down")
		idea = Ideas.get(idea_num)
		upvoters = str(len(idea["upvoters"]))
		downvoters = str(len(idea["downvoters"]))
		# Chnaging votes
		await ctx.response.edit_message(view=IdeaView(votes=[upvoters, downvoters]))


class IdeaVerdict(discord.ui.Modal):
	def __init__(self, msg, action):
		super().__init__(title=f'{"Одобрение" if action == "approve" else "Отклонение"} идеи')
		self.custom_id="idea:verdict"
		self.msg = msg
		self.action = action
		self.idea_num = msg.embeds[0].fields[0].name.split(" ")[-1]

	verdict = discord.ui.TextInput(
		label="Вердикт",
		placeholder="",
		max_length=100
	)
	async def on_submit(self, interaction: discord.Interaction):
		action_to_word = {
			"approve": "одобрена",
			"cancel": "отклонена"
		}
		action_to_emoji= {
			"approve": "🟢",
			"cancel": "🔴"
		}
		embed = self.msg.embeds[0]
		embed.set_footer(text=f"{action_to_emoji[self.action]} Идея {action_to_word[self.action]}")
		if self.verdict != "":
			embed.add_field(name=f"{Emojis.txt} Вердикт", value=self.verdict.value)
		await self.msg.edit(embed=embed, view=None)
		await self.msg.thread.edit(archived=True)
		await interaction.response.send_message(f"Идея {self.idea_num} {action_to_word[self.action]}", ephemeral=True)


class IdeaCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		bot.tree.add_command(app_commands.ContextMenu(
			name="👥 Просмотреть голоса",
			callback=self.view_voters
		))
		bot.tree.add_command(app_commands.ContextMenu(
			name="🟢 Одобрить идею",
			callback=self.apprpve_idea
		))
		bot.tree.add_command(app_commands.ContextMenu(
			name="🔴 Отклонить идею",
			callback=self.cancel_idea
		))

	@commands.hybrid_command(aliases=["швуф", "идея", "suggest", "предложить", "ыгппуые"])
	@app_commands.describe(suggestion="Идея")
	async def idea(self, ctx, *, suggestion: str):
		ideas_count = str(db.count_documents({}))
		# Building embed
		embed = discord.Embed(color=no_color)
		embed.add_field(name=f"💡 Идея {ideas_count}", value=suggestion, inline=False)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
		idea_msg = await ctx.guild.get_channel(IDEAS_CHANNEL_ID).send(embed=embed, view=IdeaView())
		await idea_msg.create_thread(name="Обсуждение", reason="Auto-thread for idea")
		Ideas.create(ideas_count, suggestion, idea_msg.id)
	@idea.error
	async def idea_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply(f"{Emojis.exclamation_mark} Пожалуйста, укажите вашу идею", allowed_mentions=no_ping)
		else:
			await ctx.reply(f"{Emojis.question_mark} Шо та произошло но я не понял что. Подробности: `{error}`", allowed_mentions=no_ping)
	
	@app_commands.default_permissions(administrator=True)
	async def view_voters(self, ctx: discord.Interaction, message:discord.Message):
		if ctx.channel.id != IDEAS_CHANNEL_ID:
			await ctx.response.send_message(f"Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
		else:
			# Setting up vars
			idea_num = message.embeds[0].fields[0].name.split(" ")[-1]
			idea = Ideas.get(idea_num)
			upvoters = "\n".join([f"<@{id}>" for id in idea["upvoters"]])
			downvoters = "\n".join([f"<@{id}>\n" for id in idea["downvoters"]])
			# Building embed
			embed = discord.Embed(title=f"{Emojis.users} Голоса", color=no_color)
			embed.add_field(name="За", value=upvoters)
			embed.add_field(name="Против", value=downvoters)
			await ctx.response.send_message(embed=embed, ephemeral=True)
	
	@app_commands.default_permissions(administrator=True)
	async def apprpve_idea(self, ctx: discord.Interaction, message:discord.Message):
		if ctx.channel.id != IDEAS_CHANNEL_ID:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
		else:
			await ctx.response.send_modal(IdeaVerdict(message, "approve"))
	
	@app_commands.default_permissions(administrator=True)
	async def cancel_idea(self, ctx: discord.Interaction, message:discord.Message):
		if ctx.channel.id != IDEAS_CHANNEL_ID:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
		else:
			await ctx.response.send_modal(IdeaVerdict(message, "cancel"))

class Ideas:
	def get(index):
		return db.find_one({"_id":index})
	
	def create(idea_num, suggestion, linked_msg_id):
		db.insert_one({
			"_id": idea_num,
			"suggestion": suggestion,
			"linked_msg_id": linked_msg_id,
			"upvoters": [],
			"downvoters": []
			})
	
	def vote(idea_num, voter, vote_type):
		# Setting up variables
		opposite_types = {
			"up": "down",
			"down": "up"
		}
		idea = Ideas.get(idea_num)
		voters_list = idea[f"{vote_type}voters"]
		opposite_voters_list = idea[f"{opposite_types[vote_type]}voters"]
		# Da voting megik
		if voter in voters_list:
			db.update_one({"_id":idea_num}, {"$pull": {f"{vote_type}voters": voter}})
		else:
			if voter in opposite_voters_list:
				db.update_one({"_id":idea_num}, {"$pull": {f"{opposite_types[vote_type]}voters": voter}})
			db.update_one({"_id":idea_num}, {"$push": {f"{vote_type}voters": voter}})
