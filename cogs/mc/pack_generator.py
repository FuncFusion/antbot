import discord

from utils.msg_utils import Emojis

import io
from json import dumps
from zipfile import ZipFile, ZIP_DEFLATED

class Templates:
	mcmeta = {"pack": {"pack_format": 0,"description": ""}}
	load_json = {"values": ["namespace:load"]}
	tick_json = {"values": ["namespace:tick"]}
	load = "say Это лоад функция"
	tick = "# Это тик функция"


class PGenerator:
	def datapack():
		dp_f = io.BytesIO()
		with ZipFile(dp_f, "w") as dp:
			dp.writestr("dp/pack.mcmeta", dumps(Templates.mcmeta))
			dp.writestr("dp/data/minecraft/tags/functions/load.json", dumps(Templates.load_json, indent="\t"))
			dp.writestr("dp/data/minecraft/tags/functions/tick.json", dumps(Templates.tick_json, indent="\t"))
			dp.writestr("dp/data/namespace/functions/load.mcfunction", Templates.load)
			dp.writestr("dp/data/namespace/functions/tick.mcfunction", Templates.tick)
		dp_f.seek(0)
		return dp_f


class Modals:
	class DP(discord.ui.Modal):
		def __init__(self):
			super().__init__(title=f"📁 Настройка датапака")
			self.custom_id="template:datapack"

		name = discord.ui.TextInput(
			label="Название",
			placeholder="Мой куртой датапак",
			max_length=64
		)
		namespaces = discord.ui.TextInput(
			label="Пространства имён",
			placeholder="my_dp, raycasts, ...",
			max_length=512
		)
		folders_include = discord.ui.TextInput(
			label="Включить папки",
			placeholder="functions, лут тейблы, tags, ...",
			max_length=512
		)
		folders_exclude = discord.ui.TextInput(
			label="Исключить папки",
			placeholder="functions, лут тейблы, tags, ...",
			max_length=512
		)
		version = discord.ui.TextInput(
			label="Версия",
			placeholder="Последняя/1.19.4/32",
			max_length=10
		)
		async def on_submit(self, ctx: discord.Interaction):
			await ctx.response.send_message(f"Aa", ephemeral=True)
	
	class RP(discord.ui.Modal):
		def __init__(self):
			super().__init__(title=f"📁 Настройка ресурспака")
			self.custom_id="template:datapack"

		name = discord.ui.TextInput(
			label="Название",
			placeholder="Мой куртой ресурспак",
			max_length=64
		)
		namespaces = discord.ui.TextInput(
			label="Пространства имён",
			placeholder="my_rp, essential, ...",
			max_length=512
		)
		folders_include = discord.ui.TextInput(
			label="Включить папки",
			placeholder="models, шейдеры, enviroment, ...",
			max_length=512
		)
		folders_exclude = discord.ui.TextInput(
			label="Исключить папки",
			placeholder="models, шейдеры, enviroment, ...",
			max_length=512
		)
		version = discord.ui.TextInput(
			label="Версия",
			placeholder="Последняя/1.19.4/27",
			max_length=10
		)
		async def on_submit(self, ctx: discord.Interaction):
			await ctx.response.send_message(f"Aa", ephemeral=True)

