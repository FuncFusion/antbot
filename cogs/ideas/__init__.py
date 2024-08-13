import discord
from discord.ext import commands
from discord import app_commands

from pymongo.mongo_client import MongoClient

from settings import IDEAS_CHANNEL_ID, MONGO_URI
from utils.general import handle_errors
from utils.msg_utils import Emojis, user_from_embed
from utils.shortcuts import no_ping, no_color


db = MongoClient(MONGO_URI).antbot.ideas

wrong_channel_errors = [
	{
		"contains": "AttributeError",
		"msg": "Не тот канал"
	},
	{
		"contains": "Wrong channel",
		"msg": "Не тот канал"
	}
]


class IdeaCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["швуф", "идея", "suggest", "предложить", "ыгппуые"],
		description="Позволяет предложить идею для сервера, публикуя её в канале `💡・идеи`.",
		usage="`/idea <идея>`",
		help="### Пример:\n`/idea Добавить канал для сэйгексинга`")
	@app_commands.describe(suggestion="Идея")
	async def idea(self, ctx, *, suggestion: str):
		ideas_count = str(db.count_documents({}))
		embed = discord.Embed(color=no_color)
		embed.add_field(name=f"💡 Идея {ideas_count}", value=suggestion, inline=False)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
		idea_msg = await ctx.guild.get_channel(IDEAS_CHANNEL_ID).send(embed=embed, view=IdeaView())
		await idea_msg.create_thread(name="Обсуждение")
		Ideas.create(ideas_count, suggestion, idea_msg.id)
		await ctx.reply(f"{Emojis.check} Идея опубликована", allowed_mentions=no_ping)
	@idea.error
	async def idea_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите вашу идею"
			}
		])
	
	@app_commands.default_permissions(administrator=True)
	@app_commands.command(name="view-voters",description="Показывает список голосующих")
	async def view_voters(self, ctx):
		if ctx.channel.parent.id != IDEAS_CHANNEL_ID:
			raise Exception("Wrong channel")
		ideas_channel = await self.bot.fetch_channel(IDEAS_CHANNEL_ID)
		ideas_message = await ideas_channel.fetch_message(ctx.channel.id)
		idea_num = ideas_message.embeds[0].fields[0].name.split(" ")[-1]
		idea = Ideas.get(idea_num)
		upvoters = "\n".join([f"<@{id}>" for id in idea["upvoters"]])
		downvoters = "\n".join([f"<@{id}>\n" for id in idea["downvoters"]])
		embed = discord.Embed(title=f"{Emojis.users} Голоса", color=no_color)
		embed.add_field(name="За", value=upvoters)
		embed.add_field(name="Против", value=downvoters)
		await ctx.response.send_message(embed=embed, ephemeral=True)
	@view_voters.error
	async def vv_error(self, ctx, error):
		await handle_errors(ctx, error, wrong_channel_errors)

	@commands.command(name="view-voters", aliases=["vv", "вью-вотерс", "посмотреть-голоса", "мшуц-мщеукы", "мм","пг"],)
	async def view_voters_pointer(self, ctx):
		await ctx.reply(f"{Emojis.exclamation_mark} Используй **слэш** команду </view-voters:1263846916798681158>", allowed_mentions=no_ping)
	
	@app_commands.default_permissions(administrator=True)
	@app_commands.command(name="approve-idea", description="Одобряет идею")
	async def approve_idea(self, ctx):
		if ctx.channel.parent.id != IDEAS_CHANNEL_ID:
			raise Exception("Wrong channel")
		ideas_channel = await self.bot.fetch_channel(IDEAS_CHANNEL_ID)
		idea_message = await ideas_channel.fetch_message(ctx.channel.id)
		idea_author_id = user_from_embed(idea_message)
		idea_author = await self.bot.fetch_user(idea_author_id)
		await idea_author.send(f"{Emojis.check} Ваша идея одобрена {idea_message.jump_url}")
		await ctx.response.send_modal(IdeaVerdict(idea_message, "approve"))
	@approve_idea.error
	async def approve_error(self, ctx, error):
		await handle_errors(ctx, error, wrong_channel_errors)

	@commands.command(name="approve-idea",
		aliases=["approve", "accept", "accept-idea", "одобрить-идею", "фззкщму-швуф", "фззкщму","фссузе"],
		description="Одобряет идею.",
		usage="`/approve-idea` (в ветке обсуждения идеи)",
		help="После введения этой команды появиться окно для введения вердикта. Автор идеи получит сообщение в лс о том, что идея была одобрена.")
	async def approve_idea_pointer(self, ctx):
		await ctx.reply(f"{Emojis.exclamation_mark} Используй **слэш** команду </approve-idea:1263846916798681159>", allowed_mentions=no_ping)
	
	@app_commands.default_permissions(administrator=True)
	@app_commands.command(name="disapprove-idea", description="Отклоняет идею")
	async def disapprove_idea(self, ctx):
		print(ctx.channel.parent.id, ctx.channel.parent.id != IDEAS_CHANNEL_ID)
		if ctx.channel.parent.id != IDEAS_CHANNEL_ID:
			raise Exception("Wrong channel")
		ideas_channel = await self.bot.fetch_channel(IDEAS_CHANNEL_ID)
		idea_message = await ideas_channel.fetch_message(ctx.channel.id)
		idea_author_id = user_from_embed(idea_message)
		idea_author = await self.bot.fetch_user(idea_author_id)
		await idea_author.send(f"{Emojis.cross} Ваша идея отклонена {idea_message.jump_url}")
		await ctx.response.send_modal(IdeaVerdict(idea_message, "cancel"))
	@disapprove_idea.error
	async def disapprove_error(self, ctx, error):
		await handle_errors(ctx, error, wrong_channel_errors)

	@commands.command(name="disapprove-idea",
		aliases=["disapprove", "deny", "deny-idea", "отклонить-идею", "вшыфззкщму-швуф", "вшыфззкщму","вутн"],
		description="Отклоняет идею.",
		usage="`/disapprove-idea` (в ветке обсуждения идеи)",
		help="После введения этой команды появиться окно для введения вердикта. Автор идеи получит сообщение в лс о том, что идея была отклонена.")
	async def disapprove_idea_pointer(self, ctx):
		await ctx.reply(f"{Emojis.exclamation_mark} Используй **слэш** команду </disapprove-idea:1263846916798681160>", allowed_mentions=no_ping)


class IdeaView(discord.ui.View):
	def __init__(self, votes=["0", "0"], disable=False):
		super().__init__(timeout=None)
		self.upvote.label = votes[0]
		self.downvote.label = votes[1]
		if disable:
			self.upvote.disabled = True
			self.downvote.disabled = True

	@discord.ui.button(label="0", emoji=Emojis.check, style=discord.ButtonStyle.grey, custom_id="ideas:upvote")
	async def upvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "up")
		idea = Ideas.get(idea_num)
		upvoters = str(len(idea["upvoters"]))
		downvoters = str(len(idea["downvoters"]))
		await ctx.response.edit_message(view=IdeaView(votes=[upvoters, downvoters]))
	
	@discord.ui.button(label="0", emoji=Emojis.cross, style=discord.ButtonStyle.grey, custom_id="ideas:downvote")
	async def downvote(self, ctx: discord.Interaction, button: discord.ui.Button):
		idea_num = ctx.message.embeds[0].fields[0].name.split(" ")[-1]
		Ideas.vote(idea_num, ctx.user.id, "down")
		idea = Ideas.get(idea_num)
		upvoters = str(len(idea["upvoters"]))
		downvoters = str(len(idea["downvoters"]))
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
		max_length=1000
	)
	async def on_submit(self, interaction: discord.Interaction):
		idea_doc = Ideas.get(self.idea_num)
		embed = self.msg.embeds[0]
		if self.verdict != "":
			embed.add_field(name=f"{Emojis.txt}{Emojis.check if self.action=='approve' else Emojis.cross} Вердикт", \
				value=self.verdict.value)
		await self.msg.edit(embed=embed, view=IdeaView(votes=[len(idea_doc["upvoters"]), len(idea_doc["downvoters"])], disable=True))
		await interaction.response.send_message(f"{Emojis.check} Идея {self.idea_num} {'одобрена' if self.action=='approve' else \
			'отклонена'}", ephemeral=True)
		await self.msg.thread.edit(archived=True)



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
		opposite_types = {
			"up": "down",
			"down": "up"
		}
		idea = Ideas.get(idea_num)
		voters_list = idea[f"{vote_type}voters"]
		opposite_voters_list = idea[f"{opposite_types[vote_type]}voters"]
		if voter in voters_list:
			db.update_one({"_id":idea_num}, {"$pull": {f"{vote_type}voters": voter}})
		else:
			if voter in opposite_voters_list:
				db.update_one({"_id":idea_num}, {"$pull": {f"{opposite_types[vote_type]}voters": voter}})
			db.update_one({"_id":idea_num}, {"$push": {f"{vote_type}voters": voter}})