import settings
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from utils import update_mcmeta_info, LazyLayout, totag

settings.GUILD = 1270326885544493076

settings.CHAT_ID = 1270326886203133965
settings.DMS_LOGS_GUILD_ID = 1204336106896752650 
settings.BOT_COMMANDS_CHANNEL_ID = 1270326886203133967
settings.CREATIONS_FORUM_ID = 1270351447116218408
settings.HELP_FORUM_ID = 1270351345714597888
settings.GIVEAWAYS_CHANNEL_ID = 1270326886391746572
settings.GIVEAWAYS_REQUESTS_CHANNEL_ID = 1270326887066898515
settings.IDEAS_CHANNEL_ID = 1276169141572730880
settings.MEDIA_CHANNEL_ID = 1290277768520663113
settings.FB_IDEAS_CHANNEL_ID = 1078066910933037106
settings.JOINS_CHANNEL_ID = 1270326886022643719
settings.LEAVES_CHANNEL_ID = 1270326886022643720
settings.LOGS_CHANNEL_ID = 1270326887066898515
settings.LOOK_FOR_CHANNEL_ID = 1270326886391746573
settings.SNAPSHOTS_CHANNEL_ID = 1270326886203133966

settings.VCS_CATEGORY_ID = 1270326886890868742
settings.CREATE_VC_CHANNEL_ID = 1270326886890868744

settings.SNAPSHOT_PING_ROLE = 1245322215428329503
settings.DATAPACK_MASTER_ROLE = 924185371225497600
settings.RESOURCEPACK_MASTER_ROLE = 940944701895356468

settings.SOLVED_TAG.id = 1270400825096929301
settings.DATAPACKS_TAG.id = 1272928452164587562
settings.ONLY_CB_TAG.id = 1419984278300786758
settings.RESOURCEPACKS_TAG.id = 1272928530962841671
settings.MISC_TAG.id = 1419984474955059292
settings.BLOCKBENCH_TAG.id = 1272928803252867153
settings.VSCODE_TAG.id = 1419983922669817946
settings.OPTIFINE_TAG.id = 1272935395465756799
settings.PLUGINS_TAG.id = 1419983503704981534
settings.MODS_TAG.id = 1285636580513550389

import discord
from discord.ext import commands

from cogs.admin import *
from cogs.faqs import *
from cogs.fun import *
from cogs.memes import *
from cogs.general import *
from cogs.giveaway import *
from cogs.help import *
from cogs.ideas import *
from cogs.logs import *
from cogs.mod import *
from cogs.minecraft import *
from cogs.voice_channels import *

logger = settings.logging.getLogger("bot")

cogs = [
	DebugCommand, EditCommand, PingCommand, StatusCommands,
	FAQs,
	EnchantCommands, LookForCommand, RandomCommands, DeadChat, TikTokCommand,
	SoyjakCommand, DemotivatorCommand, SpeechbubbleCommand, BruhCommand, GifCommand, ImpactCommand,
	HelpCommand, LinkCommand, Pin, StarterMessage, SyntaxCommand, AskToResolve, Tickets,
	JoinAndLeaveMessage, SayCommand, ServerInfoCommand, BotPing,
	GiveawayCommand, GAModerationCommands,
	Logs, IdeaVoteReactions,
	ClearCommand, PunishmentCommands, AutoThreads,
	SnapshotScraper, ColorCommand, FileCommand, MessageFormatter, PackformatCommand,
	CustomVoiceChannels
]
views = [
	LookForView, TiktokImageView,
	GifizeView, StarterMessageLayout,
	CreateTicketMessage, FileLayout
]


class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=commands.when_mentioned_or(command_prefix), case_insensitive=True)

	async def setup_hook(self):
		update_mcmeta_info.start()
		#
		self.remove_command("help")
		for cog in cogs:
			await self.add_cog(cog(self))
		for view in views:
			self.add_view(view())
		self.add_view(JudgeGA(self))
		await self.tree.sync()
		HelpCog = self.get_cog("HelpCommand")
		HelpCog.all_features.update({command.name: command.aliases for command in sorted(self.commands, key=lambda cmd: cmd.name)})
		del HelpCog.all_features['debug']

		
		logger.info(f"User: {bot.user} (ID: {bot.user.id})")
		try:
			with open("assets/pfps/online.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
		except:
			logger.warn("pfp ratelimit")

intents = discord.Intents.all()
bot = AntBot(command_prefix="!", intents=intents)
# @bot.tree.command()
# async def saygex(Interaction: discord.Interaction):
# 	await Interaction.response.send_message("say gex")

bot.run(settings.DISCORD_API_SECRET, root_logger=True)
