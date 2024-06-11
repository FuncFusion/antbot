import settings
import discord
from discord.ext import commands

from cogs.admin import EditCommand, PingCommand, StatusCommands
from cogs.faqs.faqs import FAQs
from cogs.fun import EnchantCommands, LookForCommand, RandomCommands, LookForView
from cogs.general import JoinAndLeaveMessage, RemindCommand, SayCommand, ServerInfoCommand
from cogs.help import HelpCommands, HelpListeners
from cogs.ideas import IdeaCommand, IdeaView
from cogs.logs import LogListeners
from cogs.mod import ModerationCommands
from cogs.minecraft import MessageFormatter, PackformatCommand, snapshot_scraper, TemplateCommand
from cogs.voice_channels import CustomVoiceChannels

logger = settings.logging.getLogger("bot")

cogs = [EditCommand, PingCommand, StatusCommands,
		EnchantCommands, LookForCommand, RandomCommands,	
		JoinAndLeaveMessage, RemindCommand, SayCommand, ServerInfoCommand,
	    MessageFormatter, PackformatCommand, TemplateCommand]
views = [LookForView]

class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		for cog in cogs:
			await self.add_cog(cog(self))
		for view in views:
			self.add_view(view())
		await self.add_cog(ModerationCommands(self))
		await self.add_cog(HelpCommands(self))
		await self.add_cog(HelpListeners(self))
		await self.add_cog(FAQs(self))
		await self.add_cog(IdeaCommand(self))
		self.add_view(IdeaView())
		await self.add_cog(LogListeners(self))
		await self.add_cog(CustomVoiceChannels(self))
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
