import settings
import discord
from discord.ext import commands
import asyncio

from cogs.admin import DebugCommand, EditCommand, PingCommand, StatusCommands, SayCommand
from cogs.faqs import FAQs
from cogs.fun import EnchantCommands, LookForCommand, RandomCommands, LookForView
from cogs.general import JoinAndLeaveMessage, ServerInfoCommand
from cogs.giveaway import GiveawayCommand, GAModerationCommands, JudgeGA
from cogs.help import HelpCommand, LinkCommand, Pin, PingHelpers, Ping_related_helpers, ResolveCommand, R_u_sure, StarterMessage, SyntaxCommand
from cogs.ideas import IdeaCommands, IdeaView
from cogs.logs import Logs
from cogs.mod import ClearCommand, PunishmentCommands
from cogs.minecraft import MessageFormatter, PackformatCommand, SnapshotScraper, TemplateCommand
from cogs.voice_channels import CustomVoiceChannels


logger = settings.logging.getLogger("bot")

cogs = [DebugCommand, EditCommand, PingCommand, StatusCommands,
		FAQs,
		EnchantCommands, LookForCommand, RandomCommands,	
		HelpCommand, LinkCommand, Pin, PingHelpers, ResolveCommand, StarterMessage, SyntaxCommand,
		IdeaCommands,
		JoinAndLeaveMessage, SayCommand, ServerInfoCommand,
		GiveawayCommand, GAModerationCommands,
		Logs,
		ClearCommand, PunishmentCommands,
	    MessageFormatter, PackformatCommand, SnapshotScraper, TemplateCommand,
		CustomVoiceChannels,]
views = [LookForView, IdeaView, R_u_sure, Ping_related_helpers]


class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		self.remove_command("help")
		for cog in cogs:
			await self.add_cog(cog(self))
		for view in views:
			self.add_view(view())
		self.add_view(JudgeGA(self))
		await self.tree.sync()
		HelpCog = self.get_cog("HelpCommand")
		HelpCog.all_features.update({command.name: command.aliases for command in self.commands})
		
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
