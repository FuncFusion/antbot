import settings
import discord
from discord.ext import commands
import asyncio

from cogs.admin import DebugCommand, EditCommand, PingCommand, StatusCommands, SayCommand
from cogs.faqs import FAQs
from cogs.fun import EnchantCommands, LookForCommand, RandomCommands, LookForView
from cogs.general import JoinAndLeaveMessage, ServerInfoCommand, BotPing, BotPingView
from cogs.giveaway import GiveawayCommand, GAModerationCommands, JudgeGA
from cogs.help import HelpCommand, LinkCommand, Pin, R_u_sure, StarterMessage, StarterView, SyntaxCommand
from cogs.ideas import IdeaVoteReactions
from cogs.logs import Logs
from cogs.mod import ClearCommand, PunishmentCommands, AutoThreads
from cogs.minecraft import ColorCommand, FileCommand, MessageFormatter, PackformatCommand, SnapshotScraper, TemplateCommand
from cogs.voice_channels import CustomVoiceChannels
from utils.packmcmeta import update_mcmeta_info

logger = settings.logging.getLogger("bot")

cogs = [DebugCommand, EditCommand, PingCommand, StatusCommands,
		FAQs,
		EnchantCommands, LookForCommand, RandomCommands,	
		HelpCommand, LinkCommand, Pin, StarterMessage, SyntaxCommand,
		JoinAndLeaveMessage, SayCommand, ServerInfoCommand, BotPing,
		GiveawayCommand, GAModerationCommands,
		Logs, IdeaVoteReactions,
		ClearCommand, PunishmentCommands, AutoThreads,
	    SnapshotScraper, ColorCommand, FileCommand, MessageFormatter, PackformatCommand, TemplateCommand,
		CustomVoiceChannels,]
views = [LookForView, StarterView, R_u_sure, BotPingView]


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
