import discord
from discord.ext import commands
from discord import app_commands

from settings import IDEAS_CHANNEL_ID
from utils.emojis import Emojis

from json import load, dump


class IdeaView(discord.ui.View):
	def __init__(self, votes=["0", "0"]):
		super().__init__(timeout=None)
		# Setting up variables
		self.upvote.label = votes[0]
		self.downvote.label = votes[1]

	@discord.ui.button(label="0", emoji=Emojis.mojo, style=discord.ButtonStyle.grey, custom_id="ideas:upvote")
	async def upvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		# Setting up variables
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "up")
		idea = Ideas.get()[idea_num]
		upvoters = str(len(idea["upvoters"]))
		downvoters = str(len(idea["downvoters"]))
		# Chnaging votes
		await ctx.response.edit_message(view=IdeaView(votes=[upvoters, downvoters]))
	
	@discord.ui.button(label="0", emoji=Emojis.exe, style=discord.ButtonStyle.grey, custom_id="ideas:downvote")
	async def downvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		# Setting up variables
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "down")
		idea = Ideas.get()[idea_num]
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
			embed.add_field(name="📃 Вердикт", value=self.verdict.value)
		await self.msg.edit(embed=embed, view=None)
		await interaction.response.send_message(f"Идея {self.idea_num} {action_to_word[self.action]}", ephemeral=True)


class IdeaCommand(commands.Cog):
	def __init__(self, bot):

		@bot.hybrid_command(aliases=["швуф", "идея", "suggest", "предложить", "ыгппуые"])
		async def idea(ctx, *, suggestion: str):
			ideas = Ideas.get()
			ideas_count = len(ideas)
			# Building embed
			embed = discord.Embed(color=discord.Color.dark_embed())
			embed.add_field(name=f"💡 Идея {ideas_count}", value=suggestion, inline=False)
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
			idea_msg = await ctx.guild.get_channel(IDEAS_CHANNEL_ID).send(embed=embed, view=IdeaView())
			await idea_msg.create_thread(name="Обсуждение", reason="Auto-thread for idea")
			Ideas.create(ideas_count, suggestion, idea_msg.id)
		
		@bot.tree.context_menu(name="👥 Просмотреть голоса")
		@app_commands.default_permissions(administrator=True)
		async def view_voters(ctx: discord.Interaction, message:discord.Message):
			if ctx.channel.id != IDEAS_CHANNEL_ID:
				await ctx.response.send_message(f"Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
			else:
				# Setting up vars
				idea_num = message.embeds[0].fields[0].name.split(" ")[-1]
				idea = Ideas.get()[idea_num]
				upvoters = "\n".join([f"<@{id}>" for id in idea["upvoters"]])
				downvoters = "\n".join([f"<@{id}>\n" for id in idea["downvoters"]])
				# Building embed
				embed = discord.Embed(title="👥 Голоса", color=discord.Color.dark_embed())
				embed.add_field(name="За", value=upvoters)
				embed.add_field(name="Против", value=downvoters)
				await ctx.response.send_message(embed=embed, ephemeral=True)
		
		@bot.tree.context_menu(name="🟢 Одобрить идею")
		@app_commands.default_permissions(administrator=True)
		async def view_voters(ctx: discord.Interaction, message:discord.Message):
			if ctx.channel.id != IDEAS_CHANNEL_ID:
				await ctx.response.send_message(f"Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
			else:
				await ctx.response.send_modal(IdeaVerdict(message, "approve"))
		
		@bot.tree.context_menu(name="🔴 Отклонить идею")
		@app_commands.default_permissions(administrator=True)
		async def view_voters(ctx: discord.Interaction, message:discord.Message):
			if ctx.channel.id != IDEAS_CHANNEL_ID:
				await ctx.response.send_message(f"Работает только в <#{IDEAS_CHANNEL_ID}>", ephemeral=True)
			else:
				await ctx.response.send_modal(IdeaVerdict(message, "cancel"))

class Ideas:
	def get():
		with open("cogs/ideas/ideas.json", "r", encoding="utf-8") as ideas_f:
			return load(ideas_f)
	
	def create(idea_num, suggestion, linked_msg_id):
		ideas = Ideas.get()
		ideas[idea_num] = {
			"suggestion": suggestion,
			"linked_msg_id": linked_msg_id,
			"upvoters": [],
			"downvoters": []
			}
		with open("cogs/ideas/ideas.json", "w", encoding="utf-8") as ideas_f:
			dump(ideas, ideas_f, indent="\t", ensure_ascii=False)
	
	def vote(idea_num, voter, vote_type):
		# Setting up variables
		opposite_types = {
			"up": "down",
			"down": "up"
		}
		ideas = Ideas.get()
		voters_list = ideas[idea_num][f"{vote_type}voters"]
		opposite_voters_list = ideas[idea_num][f"{opposite_types[vote_type]}voters"]
		# Da voting megik
		if voter in voters_list:
			voters_list.remove(voter)
			with open("cogs/ideas/ideas.json", "w", encoding="utf-8") as ideas_f:
				dump(ideas, ideas_f, indent="\t", ensure_ascii=False)
		else:
			if voter in opposite_voters_list:
				opposite_voters_list.remove(voter)
			voters_list.append(voter)
			with open("cogs/ideas/ideas.json", "w", encoding="utf-8") as ideas_f:
				dump(ideas, ideas_f, indent="\t", ensure_ascii=False)