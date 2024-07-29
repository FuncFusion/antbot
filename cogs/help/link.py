import discord
from discord.ext import commands
from discord import app_commands

from typing import List
from json import load

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate, all_valid


with open("assets/links.json", "r", encoding="utf-8") as f:
	links = load(f)
offered_links = [app_commands.Choice(name=links[link][0], value=link) for link in links][:25]


class LinkCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["l", "линк", "ссылка", "дштл", "ccskrf"], description="Скидывает полезную ссылку")

	async def link(self, ctx, *, resource):
		resource_link = validate(resource, links)
		if resource_link == None:
			raise Exception("Not Found")
		await ctx.reply(f"## {Emojis.link} [{links[resource_link][0]}]({resource_link})", allowed_mentions=no_ping)
	
	@link.error
	async def link_error(self, ctx, error):
		await handle_errors(ctx, error, [{
			"contains": "Not Found",
			"msg": "Ссылка по этому запросу не найдена"
		}])
	
	@link.autocomplete("resource")
	async def link_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_links
		if curr != "":
			offered_links = [app_commands.Choice(name=links[link][0], value=links[link][0]) for link in all_valid(curr, links)][:25]
		return offered_links