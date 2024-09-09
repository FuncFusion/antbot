import discord
from discord.ext import commands
from discord import app_commands

from typing import List, Literal

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.validator import validate

from utils.shortcuts import no_ping
from utils.pack_generator import Modals, PGenerator

pack_offers = (app_commands.Choice(name="Датапак", value="Датапак"), app_commands.Choice(name="Ресурспак", value="Ресурспак"))
type_offers = (app_commands.Choice(name="Базовый", value="Базовый"), app_commands.Choice(name="Расширенный", value="Расширенный"), 
	app_commands.Choice(name="Настраиваемый", value="Настраиваемый"))


class TemplateCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["tl", "темплейт", "тэмплейт", "еуьздфеу", "шаблон"],
		description="Создаёт шаблон датапака/ресурспака.",
		usage="`/template [датапак|ресурспак] [базовый|расширенный|настраиваемый]`",
		help="После введения данной команды с аргументом `настраиваемый` у вас вылезет окно, где можно указать следующие аргументы настраиваемого пака: `<название пака> [неймспейсы] [включить папки в пак (function/loot_table) (все по умолчанию)] [исключить папки в паке (function/loot_table)] [версия (последняя по умолчанию)]`\n### Пример:\n`/template custom - bth function loot_table damage_type - -`")
	@app_commands.describe(pack="Датапак/ресурспак", type="Тип пака")

	async def template(self, ctx, pack="datapack", type="basic"):
		pack_ctx = {
			"datapack": {"emoji": Emojis.deta_rack, "accusative": "датапака", "modal": Modals.DP, "function": PGenerator.datapack},
			"resourcepack": {"emoji": Emojis.resource_rack, "accusative": "ресурспака", "modal": Modals.RP, "function": PGenerator.resourcepack}
		}
		#Validating args
		if (pack:=validate(pack, {"datapack": ["dp", "дп", "датапак", "детарак", "патадак"], 
			"resourcepack": ["rp", "рп", "ресурспак", "репуксрак"]})) == None:
			raise commands.BadArgument("")
		if (type:=validate(type, {"basic": ["базовый", "стандартный", "обычный"], "extended": ["расширенный", "полный"], 
			"custom": ["кастомынй", "настраиваемый"]})) == None:
			raise commands.BadArgument("")
		#
		if type == "custom":
			await ctx.interaction.response.send_modal(pack_ctx[pack]["modal"]())
		elif type == "extended":
			await ctx.reply(f"## {pack_ctx[pack]["emoji"]} Расширенный шаблон {pack_ctx[pack]["accusative"]}", 
				file=discord.File(pack_ctx[pack]["function"](), filename=f"Extended_{pack}_(UNZIP).zip"), 
				allowed_mentions=no_ping)
		elif type == "basic":
			await ctx.reply(f"## {pack_ctx[pack]["emoji"]} Базовый шаблон {pack_ctx[pack]["accusative"]}", 
				file=discord.File(pack_ctx[pack]["function"](folders_include=["function"]), 
				filename=f"Basic_{pack}_(UNZIP).zip"), allowed_mentions=no_ping)
	
	@template.autocomplete(name="pack")
	async def template_pack_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return pack_offers
	
	@template.autocomplete(name="type")
	async def template_type_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		return type_offers

	@template.error
	async def template_error(self, ctx: commands.Context, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов"
			},
			{
				"exception": commands.BadArgument,
				"msg": "Неверный аргумент"
			},
			{
				"contains": "AttributeError",
				"msg": "Для генерации кастомного пака, используйте **слэш** команду </template:1211773146378805328>"
			}
		])

