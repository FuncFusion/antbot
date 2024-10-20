import discord
from discord.ext import commands

from asyncio import sleep
from datetime import datetime, timedelta, timezone

from settings import HELP_FORUM_ID, CREATIONS_FORUM_ID, SOLVED_TAG, DATAPACKS_TAG, RESOURCEPACKS_TAGS, \
	DATAPACK_MASTER_ROLE, RESOURCEPACK_MASTER_ROLE
from utils.msg_utils import Emojis
from utils.shortcuts import  no_color, no_ping


class StarterMessage(commands.Cog):

	@commands.Cog.listener("on_thread_create")
	async def new_help_post(self, trd):
		await sleep(0.5)
		if trd.parent_id == HELP_FORUM_ID:
			embed = discord.Embed(title=f"{Emojis.pin} Ознакомьтесь с правилами получения помощи!", color=no_color, 
				description=f"Если ещё не читали, прочитайте в закреп ветке "
				"(https://discord.com/channels/914772142300749854/1021488153909018704) рекомендации к веткам помощи, "
				"и о том, как работают некоторые её аспекты. Следование всем рекомендациям (особенно 4 пункту) поможет "
				"получить наиболее эффективную помощь. Когда проблема решится, используйте команду </resolve:1250486582109274206>.")
			await trd.send(embed=embed, view=StarterView())
		elif trd.parent_id == CREATIONS_FORUM_ID:
			embed = discord.Embed(title=f"{Emojis.pin} Ознакомьтесь с правилами творчества!", color=no_color, 
				description=f"Надеемся, что вы уже прочитали правила творчества "
				"(https://discord.com/channels/914772142300749854/1142473873200267314/1142473873200267314). "
				"Если вы хотите поменять картинку на обложке вашего поста, вы **можете это сделать**. Вы можете вставитьпрямую "
				"ссылку на картинку или ссылку на тот сайт, что уже имеет картинку в своём эмбеде. Также не забывайте, что вы можете "
				"закреплять сообщения в своей ветке, отреагировав с помощью эмодзи :pushpin:.")
			await trd.send(embed=embed)
		else:return
		await trd.starter_message.pin()


class StarterView(discord.ui.View):
	def __init__(self, disabled_mention=False):
		super().__init__(timeout=None)
		if disabled_mention:
			self.ask_for_help.disabled = True
	
	@discord.ui.button(label="Проблема решена", emoji=Emojis.check, custom_id="starter_message:resolve")
	async def resolve(self, ctx, button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(
				f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором",
				ephemeral=True,
				allowed_mentions=no_ping)
			return
		await ctx.response.send_message(
			f"{Emojis.check} Проблема решена",
			ephemeral=True,
			allowed_mentions=no_ping)
		await ctx.channel.add_tags(SOLVED_TAG)
		await ctx.channel.edit(archived=True)
	
	@discord.ui.button(label="Позвать мастеров на помощь", emoji=Emojis.question_mark, custom_id="starter_message:ask_for_help")
	async def ask_for_help(self, ctx, button):
		is_moderator = ctx.channel.permissions_for(ctx.user).manage_messages
		if ctx.user != ctx.channel.owner and not is_moderator:
			await ctx.response.send_message(
				f"{Emojis.exclamation_mark} Вы не являетесь автором этой ветки либо модератором",
				ephemeral=True,
				allowed_mentions=no_ping)
			return
		if datetime.now(tz=timezone.utc) - ctx.message.created_at < timedelta(days=1):
			await ctx.response.send_message(
				f"{Emojis.exclamation_mark} Вы сможете позвать мастеров "
				 f"<t:{int((ctx.message.created_at + timedelta(days=1)).timestamp())}:R>",
				ephemeral=True,
				allowed_mentions=no_ping)
			return
		#
		metnions = []
		if DATAPACKS_TAG in ctx.channel.applied_tags:
			metnions.append(f"<@&{DATAPACK_MASTER_ROLE}>")
		if any((tag in ctx.channel.applied_tags for tag in RESOURCEPACKS_TAGS)):
			metnions.append(f"<@&{RESOURCEPACK_MASTER_ROLE}>")
		#
		if metnions:
			await ctx.response.edit_message(view=StarterView(disabled_mention=True))
			await ctx.channel.send(" ".join(metnions))
		else:
			await ctx.response.send_message(
				f"{Emojis.exclamation_mark} Не обнаружено дп/рп тэгов в этом посте", 
				ephemeral=True)

