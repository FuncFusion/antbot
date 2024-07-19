import discord
from discord.ext import commands
from discord import app_commands

from typing import List, Literal

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.validator import validate

from utils.shortcuts import no_ping
from utils.pack_generator import Modals


class TemplateCommand(commands.Cog):
	@commands.hybrid_command(aliases=["tl", "темплейт", "тэмплейт", "еуьздфеу", "шаблон"],
		description="Создаёт шаблон датапака/ресурспака")
	@app_commands.describe(template="Датапак/ресусрпак", type="Тип пака")

	async def template(self, ctx, template:Literal["Датапак", "Ресурспак"]="datapack", 
		type:Literal["Базовый", "Расширенный", "Настраиваемый"]="basic"):
		pack_ctx = {
			"datapack": {"emoji": Emojis.deta_rack, "accusative": "датапака", "modal": Modals.DP},
			"resourcepack": {"emoji": Emojis.resource_rack, "accusative": "ресурспака", "modal": Modals.RP}
		}
		#Validating args
		if (v_template:=validate(template, {"datapack": ["dp", "дп", "датапак", "детарак", "патадак"], "resourcepack": ["rp", "рп", "ресурспак", "репуксрак"]}))\
			!= None:
			template = v_template
		else:
			raise commands.BadArgument(template)
		if (v_type:=validate(type, {"basic": ["базовый", "стандартный", "обычный"], "extended": ["расширенный", "полный"], "custom": ["кастомынй", "настраиваемый"]}))\
			!= None:
			type = v_type
		else:
			raise commands.BadArgument(type)
		for arg in [template, type]:
			if arg == None:
				raise commands.BadArgument(f"{arg}")
		#
		if type == "custom":
			await ctx.interaction.response.send_modal(pack_ctx[template]["modal"]())
		elif type == "extended":
			with open(f"assets/templates/Extended {template}.zip", "rb") as pack:
				await ctx.reply(f"{pack_ctx[template]["emoji"]} Расширенный шаблон {pack_ctx[template]["accusative"]}", 
				file=discord.File(pack, filename=f"Extended_{template}_(UNZIP).zip"), allowed_mentions=no_ping)
		elif type == "basic":
			with open(f"assets/templates/Basic {template}.zip", "rb") as pack:
				await ctx.reply(f"{pack_ctx[template]["emoji"]} Базовый шаблон {pack_ctx[template]["accusative"]}", 
				file=discord.File(pack, filename=f"Basic_{template}_(UNZIP).zip"), allowed_mentions=no_ping)

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
			}
		])

