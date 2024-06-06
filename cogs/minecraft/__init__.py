import discord
from discord.ext import commands
from discord import app_commands

from typing import List

from utils.general import handle_errors
from utils.msg_utils import Emojis

from cogs.minecraft.message_formatter import formatter_listener
from cogs.minecraft.snapshot_scraper import snapshot_scraper
from cogs.minecraft.packformat import packformat_command
from cogs.minecraft.template import template_command

class Minecraft(commands.Cog):
	@commands.hybrid_command(aliases=["mcmetaformat",
		"pack-format", "pack_format", "packmcmetaformat",
		"pf", "пакформат", "пак-формат", "пак_формат", 
		"мсметаформат", "пакмсметаформат","пф", "зфслащкьфе", "за"], 
		description="Выдаёт актуальные числа, которые соответствуют версиям в pack_format")
	@app_commands.describe(type="Показать числа для ресурспака или датапака", 
		show_all="Показать числа для всех версий и снапшотов")
	async def packformat(self, ctx, type, *, show_all=""):
		await packformat_command(ctx, type, show_all)
	@packformat.error
	async def packformat_error(self, ctx, error: Exception):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Не хватает аргументов"
			},
			{
				"contains": "AttributeError",
				"msg": f"{Emojis.exclamation_mark} Неверно указан тип пакформата"
			}
		])

	@commands.hybrid_command(aliases=["tl", "темплейт", "тэмплейт", "еуьздфеу", "шаблон"],
		description="Создаёт шаблон датапака/ресурспака")
	@app_commands.describe(template="Датапак/ресусрпак", type="Тип пака")
	async def template(self, ctx, template: str="datapack", type: str="basic"):
		await template_command(ctx, template, type)
	@template.error
	async def template_error(self, ctx: commands.Context, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Не хватает аргументов"
			},
			{
				"exception": commands.BadArgument,
				"msg": f"{Emojis.exclamation_mark} Неверный аргумент"
			}
		])
	@template.autocomplete("template")
	async def template_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return [app_commands.Choice(name="Датапак", value="datapack"), app_commands.Choice(name="Ресурспак", value="resourcepack")]
	@template.autocomplete("type")
	async def template_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return [app_commands.Choice(name="Базовый", value="basic"), app_commands.Choice(name="Расширенный", value="extended"),
		  app_commands.Choice(name="Настраиваемый", value="custom")]

	@commands.Cog.listener("on_message")
	async def formatter(self, msg):
		await formatter_listener(msg)
