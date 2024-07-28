import discord
from discord.ext import commands
from discord import app_commands

from typing import List
from json import load

from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate, least_distance


with open("assets/links.json", "r", encoding="utf-8") as f:
	links = load(f)
offered_links = [app_commands.Choice(name=links[link][0], value=link) for link in links][:25]


class LinkCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(aliases=["линк", "ссылка", "дштл", "ccskrf"], description="Скидывает полезную ссылку")
	async def link(self, ctx, *, resource):
		resource_link = validate(resource, links)
		# embed = discord.Embed(description=, color=no_color)
		await ctx.reply(f"## {Emojis.link} [{links[resource_link][0]}]({resource_link})", allowed_mentions=no_ping)
	
	@link.autocomplete("resource")
	async def link_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_links
		if curr != "":
			offered_links = [app_commands.Choice(name=links[link][0], value=link) for link in links if least_distance(curr, links) <= len(link)/2][:25]
		return offered_links