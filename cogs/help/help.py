import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING
import os
from re import search, MULTILINE
from typing import List

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate, all_valid, closest_match


class HelpCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.all_features = special_features.copy()
	
	@commands.hybrid_command(
		aliases=["h", "?", "х", "хелп", "помощь", "рудз"], 
		description="Показывает, как пользоваться командами/фичами антбота.",
		usage="`/help <название команды/фичи>`",
		help="Написав просто `/help`, вы получите список всех доступных команд и фич. Написав конкретное название фичи, получите подробное описание её использования.\n### Пример:\n`/help форматтер`")
	async def help(self, ctx, *, feature=None):
		fetched_commands = await self.bot.tree.fetch_commands()
		if feature == None:
			permed_cmd_list = []
			for command in fetched_commands:
				if command.default_member_permissions is None:
					permed_cmd_list.append(command)
				elif ctx.channel.permissions_for(ctx.author) >= command.default_member_permissions:
					permed_cmd_list.append(command)
			cmd_mentions = ", ".join([f"{command.mention}" for command in sorted(permed_cmd_list, key=lambda command: command.name)])
			special_feature_list = "\n".join([f"**`{special_feature}`**" for special_feature in special_features])
			thumbnail = discord.File("assets/antbot.png", filename="antbot.png")
			embed = discord.Embed(color=no_color)
			embed.set_thumbnail(url="attachment://antbot.png")
			embed.description = f"## Команды:\n{cmd_mentions}\n## Фичи:\n{special_feature_list}\n"
			await ctx.reply(embed=embed, file=thumbnail, allowed_mentions=no_ping)
			return
		feature = closest_match(feature, self.all_features, 10)
		if feature == None:
			raise AttributeError
		embed = discord.Embed(color=no_color)
		for command in self.bot.commands:
			if feature == command.name or feature in command.aliases:
				mention = f"**/{command.name}**"
				for cmd in fetched_commands:
					if command.name == cmd.name:
						mention = cmd.mention
				aliases = ", ".join([f"`{alias}`" for alias in command.aliases])
				try:
					image = discord.File(f"assets/help/{command.name}.png", filename="image.png")
				except:
					image = MISSING

				embed.description = f"## {Emojis.md} Команда {mention}\n{command.description}\n### Алиасы:\n{aliases}\n### Использование:\n{command.usage}\n\n{command.help}"
				embed.set_image(url="attachment://image.png")
				await ctx.reply(embed=embed, file=image, allowed_mentions=no_ping)
				return
			elif feature in special_features.keys():
				special_feature_name = special_features[feature][0]
				try:
					image = discord.File(f"assets/help/{special_feature_name}.png", filename="image.png")
				except:
					image = MISSING
				description = special_feature_descs[special_feature_name]
				embed.description = f"## {Emojis.md} {feature}\n{description}"
				embed.set_image(url="attachment://image.png")
				await ctx.reply(embed=embed, file=image, allowed_mentions=no_ping)
				return
	
	@help.autocomplete("feature")
	async def help_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		if curr != "":
			return [app_commands.Choice(name=feature, value=feature) for feature in all_valid(curr, self.all_features)][:25]
		else:
			return [app_commands.Choice(name=feature, value=feature) for feature in list(self.all_features)][:25]

	@help.error
	async def help_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов. Используй </help:1269737191353876480> что бы просмотреть возможные опции"
			},
			{
				"contains": "AttributeError",
				"msg": "Не существует такой команды/фичи"
			}
		])

special_features = {
	"Форматтер": ["formatter", "форматтер сообщений", "хайлайтер", "генератор древа файлов", "highlighter", 
		"tree generator", "форматирование"],
	"Закреп в своих ветках помощи/творчества": ["pin", "закреп", "пин", "закрепить", "закрепи", "закрепить ветку", "закрепить ветку помощи"],
	"Система собственных голосовых каналов": ["voice-channels","система гк", "кастом гк", "гк", "свои гк", "голосовые каналы"],
	"FAQшки": ["faqshki", "faqшки", "факушки", "факу", "faq"],
	"Уведомление о выходе новой версии майна": ["snapshot-scraper","новые снапшоты","снапшот скрейпер","new snapshots","снапшоты"]
}

special_feature_descs = {}
for filename in os.listdir("assets/help"):
	if filename.endswith(".md"):
		with open(f"assets/help/{filename}", "r", encoding="utf-8") as file:
			special_feature_descs[filename.replace(".md", "")] = file.read()

