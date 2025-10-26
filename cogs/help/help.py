import discord
from discord.ext import commands
from discord.utils import MISSING
from discord import app_commands, ui

import os
from re import search, MULTILINE
from typing import List

from utils import handle_errors, Emojis, no_ping, validate, all_valid, closest_match, LazyLayout


class HelpCommand(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
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
			special_feature_list = "\n".join([f"- **`{special_feature}`**" for special_feature in special_features])

			await ctx.reply(
				view=LazyLayout(
					ui.Section(
						f"## Команды:\n{cmd_mentions}\n## Фичи:\n{special_feature_list}\n",
						accessory=ui.Thumbnail(self.bot.user.avatar.url)
					)
				),
				allowed_mentions=no_ping
			)
			return
		
		feature = closest_match(feature, self.all_features, 10)
		if feature == None:
			raise AttributeError

		image = MISSING
		for command in self.bot.commands:
			if feature == command.name or feature in command.aliases:
				mention = f"**/{command.name}**"
				for cmd in fetched_commands:
					if command.name == cmd.name:
						mention = cmd.mention
				aliases = ", ".join([f"`{alias}`" for alias in command.aliases])
				try:
					image = discord.File(f"assets/help/{command.name}.png", filename="image.png")
				except:pass

				layout = LazyLayout(
					ui.TextDisplay(
						f"## {Emojis.md} Команда {mention}\n{command.description}\n"
						f"### Алиасы:\n{aliases}\n### Использование:\n{command.usage}\n\n{command.help}"
					)
				)
				break
			
			elif feature in special_features.keys():
				special_feature_name = special_features[feature][0]
				try:
					image = discord.File(f"assets/help/{special_feature_name}.png", filename="image.png")
				except:pass
				description = special_feature_descs[special_feature_name]
				layout = LazyLayout(
					ui.TextDisplay(f"## {Emojis.md} {feature}\n{description}")
				)
				break
			
		if image:
			layout.children[0].add_item(
				ui.MediaGallery(
					discord.MediaGalleryItem("attachment://image.png")
				)
			)
		await ctx.reply(
			view=layout, 
			file=image, 
			allowed_mentions=no_ping
		)
	
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
	"Система собственных голосовых каналов": ["voice-channels","система гк", "кастом гк", "гк", "свои гк", "голосовые каналы", "vc", "custom vcs"],
	"FAQшки": ["faqshki", "faqшки", "факушки", "факу", "faq"],
	"Уведомление о выходе новой версии майна": ["snapshot-scraper","новые снапшоты","снапшот скрейпер","new snapshots","снапшоты"]
}

special_feature_descs = {}
for filename in os.listdir("assets/help"):
	if filename.endswith(".md"):
		with open(f"assets/help/{filename}", "r", encoding="utf-8") as file:
			special_feature_descs[filename.replace(".md", "")] = file.read()

