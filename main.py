import settings
import discord
from discord.ext import commands
import asyncio

from cogs.admin import DebugCommand, EditCommand, PingCommand, StatusCommands, SayCommand
from cogs.faqs import FAQs
from cogs.fun import EnchantCommands, LookForCommand, RandomCommands, LookForView
from cogs.general import JoinAndLeaveMessage, RemindCommand, ServerInfoCommand
from cogs.giveaway import GiveawayCommand, GAModerationCommands, JudgeGA
from cogs.help import LinkCommand, Pin, ResolveCommand, R_u_sure, StartMessage, SyntaxCommand
from cogs.ideas import IdeaCommands, IdeaView
from cogs.logs import Logs
from cogs.mod import ClearCommand, PunishmentCommands
from cogs.minecraft import MessageFormatter, PackformatCommand, snapshot_scraper, TemplateCommand
from cogs.voice_channels import CustomVoiceChannels

logger = settings.logging.getLogger("bot")

cogs = [DebugCommand, EditCommand, PingCommand, StatusCommands,
		FAQs,
		EnchantCommands, LookForCommand, RandomCommands,	
		LinkCommand, Pin, ResolveCommand, StartMessage, SyntaxCommand,
		IdeaCommands,
		JoinAndLeaveMessage, SayCommand, ServerInfoCommand,
		GiveawayCommand, GAModerationCommands,
		Logs,
		ClearCommand, PunishmentCommands,
	    MessageFormatter, PackformatCommand, TemplateCommand,
		CustomVoiceChannels,]
views = [LookForView, IdeaView, R_u_sure]



class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		for cog in cogs:
			await self.add_cog(cog(self))
		for view in views:
			self.add_view(view())
		self.add_view(JudgeGA(self))
		await self.tree.sync()
		
		logger.info(f"User: {bot.user} (ID: {bot.user.id})")
		try:
			with open("assets/pfps/online.png", "rb") as file:
				await bot.user.edit(avatar=file.read())
		except:
			logger.warn("pfp ratelimit")

intents = discord.Intents.all()
bot = AntBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	# snapshot scraper
	snapshot_channel = await bot.fetch_channel(settings.SNAPSHOTS_CHANNEL_ID)
	await snapshot_scraper(snapshot_channel)

@bot.tree.command()
async def saygex(Interaction: discord.Interaction):
	await Interaction.response.send_message("say gex")

	
bot.run(settings.DISCORD_API_SECRET, root_logger=True)
