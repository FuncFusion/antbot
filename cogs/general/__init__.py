from cogs.general.join_leave_messages import JoinAndLeaveMessage
from cogs.general.remind import RemindCommand
from cogs.general.say import SayCommand
from cogs.general.serverinfo import ServerInfoCommand


# help_attrs = {'name': 'help', 'aliases': ["helps", "хелп", "h", "рудз", "рудзы", "х", "р"]}
# class CustomHelpCommand(commands.HelpCommand):

# 	async def send_bot_help(self, mapping):
# 		embed = discord.Embed(title="Список команд AntBot-a", color=no_color)
# 		thumbnail = discord.File("assets/pfps/online.png", filename="online.png")
# 		embed.set_thumbnail(url="attachment://online.png")
# 		for cog, cmds in mapping.items():
# 			cmd_str = ", ".join(f"`{cmd.name}`" for cmd in cmds)
# 			cmd_signature = [self.get_command_signature(cmd) for cmd in cmds]
# 			cog_name = getattr(cog, "qualified_name", "no_help")
# 			if not cog_name.startswith("no_help"):
# 				embed.add_field(name=cog_name, value=cmd_str, inline=False)
# 		await self.context.reply(embed=embed, file=thumbnail, allowed_mentions=no_ping)
	
# 	async def send_command_help(self, cmd):
# 		embed = discord.Embed(title=f"Команда `{cmd.name}`", color=no_color)
# 		embed.description = cmd.description
# 		params = ""
# 		if cmd.clean_params != {}: params = " " + " ".join(f"[{param}]" for param in cmd.clean_params)
# 		embed.add_field(name="Использование", value=f"`{self.context.clean_prefix}{cmd.name}{params}`", inline=False)
# 		alias_str = ", ".join(f"`{alias}`" for alias in cmd.aliases)
# 		embed.add_field(name="Алиасы", value=alias_str, inline=False)
# 		await self.context.reply(embed=embed, allowed_mentions=no_ping)
	
# 	async def command_not_found(self, string: str) -> str:
# 		possible_cmds, assumption = [], ""
# 		for cmd in self.context.bot.commands:
# 			if distance(string, cmd.name) <= len(cmd.name)/2:
# 				possible_cmds.append(cmd.name)
# 		if possible_cmds != []:
# 			cmds_str = "\n".join(f"`{cmd}`" for cmd in possible_cmds)
# 			assumption = f" Возможно, вы имели ввиду:\n{cmds_str}"
# 		await self.context.reply(f"Не нашёл такой команды - `{string.replace('`', ' ')}`.{assumption}", allowed_mentions=no_ping)

# 	async def subcommand_not_found(self, cmd, string) -> str:
# 		await CustomHelpCommand.send_command_help(self, cmd)

# 	async def send_cog_help(self, cog):
# 		await CustomHelpCommand.command_not_found(self, cog.qualified_name)


# class GeneralCommands(commands.Cog, name="Общие"):
# 	def __init__(self, bot):
# 		self._original_help_command = bot.help_command
# 		bot.help_command = CustomHelpCommand(command_attrs=help_attrs)
# 		bot.help_command.cog = self
# 		self.bot = bot

	# def cog_unload(self):
	# 	self.bot.help_command = self._original_help_command
