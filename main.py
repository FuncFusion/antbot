import settings
import discord
from discord.ext import commands

from cogs.general import GeneralCommands
from cogs.fun import FunCommands
from cogs.admin import AdminCommands
from cogs.minecraft import MinecraftCommands
from cogs.mod import ModerationCommands
from cogs.help import HelpCommands, HelpListeners
from cogs.faqs.faqs import FAQs

logger = settings.logging.getLogger("bot")


class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		await self.add_cog(GeneralCommands(self))
		await self.add_cog(FunCommands(self))
		await self.add_cog(AdminCommands(self))
		await self.add_cog(MinecraftCommands(self))
		await self.add_cog(ModerationCommands(self))
		await self.add_cog(HelpCommands(self))
		await self.add_cog(HelpListeners(self))
		await self.add_cog(FAQs(self))
		await self.tree.sync()

intents = discord.Intents.all()
bot = AntBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	with open("assets/pfps/online.png", "rb") as file:
		await bot.user.edit(avatar=file.read())
	logger.info(f"User: {bot.user} (ID: {bot.user.id})")
	
@bot.tree.command()
async def saygex(Interaction: discord.Interaction):
	await Interaction.response.send_message("gex")

	
bot.run(settings.DISCORD_API_SECRET, root_logger=True)
