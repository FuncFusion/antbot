import settings
import discord
from discord.ext import commands

from cogs.general import GeneralCommands
from cogs.fun import FunCommands
from cogs.admin import AdminCommands

logger = settings.logging.getLogger("bot")


class AntBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		await self.add_cog(GeneralCommands(self))
		await self.add_cog(FunCommands(self))
		await self.add_cog(AdminCommands(self))
		await self.tree.sync()

intents = discord.Intents.all()
bot = AntBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	logger.info(f"User: {bot.user} (ID: {bot.user.id})")

@bot.command(aliases=['p', 'зштп', 'пинг'])
async def ping(ctx):
	await ctx.send("brbr")
	
@bot.tree.command()
async def saygex(Intercation: discord.Interaction):
	await Intercation.response.send_message("gex")

	
bot.run(settings.DISCORD_API_SECRET, root_logger=True)
