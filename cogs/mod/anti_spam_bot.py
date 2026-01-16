import discord
from discord.ext import commands
from discord import ui
from settings import ANTI_SPAM_CHANNEL_ID, MODERATOR_ONLY_CHANNEL_ID, CHAT_ID
from utils.general import is_moderator
from utils import LazyLayout
from utils.msg_utils import Emojis, no_ping
from random import choice


class AntiSpamBot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener("on_message")
	async def anti_spam_bot(self, msg: discord.Message):
		if msg.channel.id != ANTI_SPAM_CHANNEL_ID:
			return
		if msg.author.bot or is_moderator(msg.author):
			return
		spam_bot_user = msg.author
		mod_only_chnl = await msg.guild.fetch_channel(MODERATOR_ONLY_CHANNEL_ID)
		await mod_only_chnl.send(
			view=LazyLayout(
				ui.Section(
					f"# {Emojis.ban} Бан\n"
					f"**Забаненый участник**\n{spam_bot_user.name}({spam_bot_user.mention})\n"
					f"**Причина**\nБот спамер\n"
					f"**Сообщение**\n{msg.clean_content}",
					accessory=ui.Thumbnail(spam_bot_user.display_avatar.url)
				)
			), 
			allowed_mentions=no_ping
		)

		kick_msgs = [
			f"Спамер {spam_bot_user.name} ({spam_bot_user.mention}) был забанен <:smirk_new:1311716402742296689>",
			f"Минус один бот скамер — {spam_bot_user.name} ({spam_bot_user.mention}) был забанен",
			f"{spam_bot_user.name} ({spam_bot_user.mention}) был дезинтегрирован <:smirk_new:1311716402742296689>",
			f"Казино от мистера биста это конечно хорошо, но вам тут не место — {spam_bot_user.name} ({spam_bot_user.mention}) был забанен",
			f"{spam_bot_user.name} ({spam_bot_user.mention}) забанен :index_pointing_at_the_viewer::joy:"
		]
		chat_chnl = await msg.guild.fetch_channel(CHAT_ID)
		await chat_chnl.send(choice(kick_msgs),allowed_mentions=no_ping)

		await spam_bot_user.ban(reason="Бот спамер",delete_message_seconds=3600)
		await msg.delete()
