import discord
from discord.ext import commands
from settings import HELP_FORUM_ID
from utils.validator import validate
from utils.general import get_help_thread_author

class AskToResolve(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_message")
	async def ask_to_resolve(self, msg: discord.Message):
		if not isinstance(msg.channel.parent, discord.ForumChannel) \
			or isinstance(msg.channel.parent, discord.ForumChannel) and msg.channel.parent_id != HELP_FORUM_ID:
			return
		post_author = await get_help_thread_author(msg)
		if msg.author != post_author:
			return
		valid_strings = {
			"решено": ["решил", "решила", "решили", "решилось"],
			"спасибо": ["спс", "благодарю", "спасибки", "пасиб", "благодарствую", "благодарен"],
			"помогло": ["помог", "помогла", "помогли"],
			"разобрался": ["разобралась", "разобрались", "понял", "поняла"]
		}
		msg_words = msg.content.strip().lower().split()
		if "не" not in msg.content.lower() and any(validate(word, valid_strings, 4) for word in msg_words):
			await self.ask_to_resolve_msg(msg)
	
	@commands.Cog.listener("on_raw_reaction_add")
	async def ask_to_resolve_reaction(self, reaction):
		chnl = self.bot.get_channel(reaction.channel_id)
		msg = await chnl.fetch_message(reaction.message_id)
		if chnl.parent_id != HELP_FORUM_ID:
			return
		post_author = await get_help_thread_author(msg)
		if msg.author != post_author:
			return
		elif reaction.emoji.name != "check":
			return
		await self.ask_to_resolve_msg(msg)

	async def ask_to_resolve_msg(self, msg):
		first_msgs = [msg async for msg in msg.channel.history(oldest_first=True) if msg.author.bot]
		if not first_msgs:
			return
		first_msg = first_msgs[0]
		existing_ask_msgs = [msg async for msg in msg.channel.history() 
						if msg.author.bot and "если ваша проблема решена" in msg.content]
		if len(existing_ask_msgs) < 2:
			await first_msg.reply(f"{msg.author.mention}, если ваша проблема решена, нажмите на соответствующую кнопку у того сообщения. Если вы думаете, что будете ещё задавать связанные с этой темой вопросы в этой ветке, то можете пока не нажимать.")