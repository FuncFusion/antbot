import discord
from discord.ext import commands
from discord import app_commands

from typing import List
from json import load

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import closest_match, all_valid
from settings import DMS_LOGS_GUILD_ID
import re


with open("assets/links.json", "r", encoding="utf-8") as f:
	links = load(f)
offered_links = [app_commands.Choice(name=links[link][0], value=links[link][0]) for link in links][:25]


class LinkCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		aliases=["l", "л", "линк", "ссылка", "дштл", "ccskrf", "resource","ресурс","д"],
		description="Скидывает ссылку на ресурс.",
		usage="`/link <название ресурса>`",
		help="Написав просто `/link`, в автокомплите увидите список доступных ресурсов. Там максимум может отображаться 25 элементов, поэтому просто начните писать название ресурса, и он там появится. Вы можете предлагать полезные ресурсы для добавления в бота в канале `🐜・antbot`.\n### Пример:\n`/link dp essentials`")

	async def link(self, ctx, *, resource):
		resource_link = closest_match(resource, links, 10)
		if resource_link == None:
			raise AttributeError("Not Found")
		await ctx.reply(f"## {Emojis.link} [{links[resource_link][0]}]({resource_link})", allowed_mentions=no_ping)

	@commands.Cog.listener("on_message")
	async def link_msg(self, msg):
		if msg.author.bot:
			return
		if msg.guild != None and msg.guild.id == DMS_LOGS_GUILD_ID:
			return
		segments = re.findall(r'(?:\*\*[Llлл]\*\*)([^?*]+)(?:\*\*[Llлл]\*\*)*?', msg.content)
		if segments == []:
			return
		args = []
		for segment in segments:
			words = re.findall(r'\S+', segment)
			for i in range(len(words)):
				args.append(' '.join(words[:i+1]))
		resource_links = []
		for arg in args:
			resource_name = closest_match(arg, links, accuracy=12)
			if resource_name != None and resource_name not in resource_links:
				print(arg, resource_name)
				resource_links.append(resource_name)
		if resource_links == []:
			await handle_errors(msg, AttributeError("Not Found"), [{
				"exception": AttributeError,
				"msg": "Ссылка по этому запросу не найдена"
			}])
		for resource_link in resource_links[:3]:
			await msg.reply(f"## {Emojis.link} [{links[resource_link][0]}]({resource_link})", allowed_mentions=no_ping)
	
	@link.error
	async def link_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Пожалуйста, укажите название ресурса. Используйте **слэш** команду </link:1267188435492405359>, где в автокомплите будет видно список доступных ресурсов."
			},
			{
				"contains": "Not Found",
				"msg": "Ссылка по этому запросу не найдена"
			}
		])
	
	@link.autocomplete("resource")
	async def link_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_links
		if curr != "":
			return [app_commands.Choice(name=links[link][0], value=links[link][0]) for link in all_valid(curr, links)][:25]
		else:
			return offered_links