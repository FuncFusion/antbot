import discord

from utils.msg_utils import Emojis
from utils.validator import validate

import io
from string import ascii_lowercase, digits
from json import dumps
from zipfile import ZipFile, ZIP_DEFLATED
from Levenshtein import distance

class Templates:
	mcmeta = '{{\n\t"pack": {{\n\t\t"pack_format": {0},\n\t\t"description": "https://discord.gg/anthill-914772142300749854"\n\t}}\n}}'
	load_json = {"values": ["namespace:load"]}
	tick_json = {"values": ["namespace:tick"]}
	load = "say Это лоад функция"
	tick = "# Это тик функция"
	custom_model_data = '{{\n\t"parent": "item/generated",\n\t"textures": {{\n\t\t"layer0": "<путь к текстуре>"\n\t}},\n\t"overrides": [\n\t\t{{ "predicate": {{ "custom_model_data": {0} }}, "model": "item/cosmetics/eye_patch"}},\n\t]}}'


class PGenerator:
	def validate_folders(folders, type):
		dp_folders = {
			"advancement": ["адванцмент", "ачивки", "достижения"],
			"chat_type": ["чат тайп", "тип чата"],
			"damage_type": ["дэмедж тайп", "тип урона"],
			"dimension": ["дименшон", "измерение"],
			"dimension_type": ["дименшон тайп", "тип измерения"],
			"loot_tables": ["лут тейблы", "таблицы лута", "таблицы добычи"],
			"predicates": ["предикейтс", "предикаты"],
			"recipes": ["ресипис", "рецепты", "рецепты крафта"],
			"structures": ["стракчерс", "структуры", "данжи"],
			"tags": ["тэгс", "теги", "ярлыки"],
			"worldgen": ["ворлдген", "генерация", "генерация мира"]
			}
		rp_folders = {
			"atlases": ["атласы"],
			"blockstates": ["блокстейтс", "блок стейты", "состояния блоков"],
			"font": ["фонт", "шрифт"],
			"lang": ["лэнг", "язык"],
			"modles": ["моделс", "модели"],
			"particles": ["партиклс", "партиклы", "частицы"],
			"shaders": ["шейдерс", "шейдеры", "тёмная магия"],
			"texts": ["текстс", "текста", "строки"],
			"textures": ["тещурс", "текстуры"]
		}
		existing_fldrs = dp_folders if type == "dp" else rp_folders
		valid_folders = set()
		for folder in folders:
			valid_folder = validate(folder, existing_fldrs)
			if valid_folder != None:
				valid_folders.add(valid_folder)
		return list(valid_folders)
	
	def validate_namespaces(namespaces):
		valid_chars = ascii_lowercase + digits + "_-" 
		valid_namespaces = set()
		curr_nspc = ""
		for nspc in namespaces:
			for char in nspc:
				if char in valid_chars:
					curr_nspc += char
			if curr_nspc != "":
				valid_namespaces.add(curr_nspc)
		return list(valid_namespaces)

	def datapack(name="детарак", namespaces=["namespace"], folders_include=[], folders_exclude=[], version=32):
		# Validating stuff
		folders_include = PGenerator.validate_folders(folders_include, "dp")
		folders_exclude = PGenerator.validate_folders(folders_exclude, "dp")
		namespaces = PGenerator.validate_namespaces(namespaces)
		main_namespace = "namespace" if namespaces == [] else namespaces[0]
		all_folders = ["advancement", "chat_type", "damage_type", "dimension", "dimension_type", "functions", "loot_tables", "predicates", "recipes", "structures", "tags", "worldgen"]
		# Generating dp
		dp_f = io.BytesIO()
		with ZipFile(dp_f, "w") as dp:
			dp.writestr(f"{name}/pack.mcmeta", Templates.mcmeta.format(version))
			dp.writestr(f"{name}/data/minecraft/tags/functions/load.json", dumps(Templates.load_json, indent="\t"))
			dp.writestr(f"{name}/data/minecraft/tags/functions/tick.json", dumps(Templates.tick_json, indent="\t"))
			dp.writestr(f"{name}/data/{main_namespace}/functions/load.mcfunction", Templates.load)
			dp.writestr(f"{name}/data/{main_namespace}/functions/tick.mcfunction", Templates.tick)
			for namespace in namespaces:
				dp.mkdir(f"{name}/data/{namespace}")
			if folders_exclude == []:
				if folders_include == []:
					for folder in all_folders:
						dp.mkdir(f"{name}/data/{main_namespace}/{folder}")
				else:
					for folder in folders_include:
						dp.mkdir(f"{name}/data/{main_namespace}/{folder}")
		dp_f.seek(0)
		return dp_f
	
	def resourcepack(name="репуксрак", namespaces=[], folders_include=[], folders_exclude=[], version=32):
		# Validating stuff
		all_folders = ["atlases", "blockstates", "font", "lang", "models", "particles", "shaders", "texts", "textures"]
		folders_include = PGenerator.validate_folders(folders_include, "rp"); folders_include = folders_include if folders_include != [] else all_folders
		folders_exclude = PGenerator.validate_folders(folders_exclude, "rp")
		namespaces = PGenerator.validate_namespaces(namespaces)
		main_namespace = "namespace" if namespaces == [] else namespaces[0]
		# Generating rp
		rp_f = io.BytesIO()
		with ZipFile(rp_f, "w") as rp:
			rp.writestr(f"{name}/pack.mcmeta", Templates.mcmeta.format(version))
			if "models" in folders_include:
				rp.writestr(f"{name}/assets/minecraft/models/item/custom_model_data.json", Templates.custom_model_data.format(str(version)))
			for namespace in namespaces:
				rp.mkdir(f"{name}/assets/{namespace}")
			if folders_exclude == []:
				for folder in folders_include:
					rp.mkdir(f"{name}/assets/minecraft/{folder}")
		rp_f.seek(0)
		return rp_f


class Modals:
	class DP(discord.ui.Modal):
		def __init__(self):
			super().__init__(title=f"📁 Настройка датапака")
			self.custom_id="template:datapack"

		name = discord.ui.TextInput(
			required=False,
			label="Название",
			placeholder="Мой куртой датапак",
			max_length=64
		)
		namespaces = discord.ui.TextInput(
			required=False,
			label="Пространства имён",
			placeholder="my_dp, raycasts, ...",
			max_length=512
		)
		folders_include = discord.ui.TextInput(
			required=False,
			label="Включить папки (все по умолчанию)",
			placeholder="functions, лут тейблы, tags, ...",
			max_length=512
		)
		folders_exclude = discord.ui.TextInput(
			required=False,
			label="Исключить папки",
			placeholder="functions, лут тейблы, tags, ...",
			max_length=512
		)
		version = discord.ui.TextInput(
			required=False,
			label="Версия",
			placeholder="Последняя/1.19.4/32",
			max_length=10
		)
		async def on_submit(self, Interaction: discord.Interaction):
			dp = PGenerator.datapack(
				self.name.value if self.name.value != "" else "datapak", 
				self.namespaces.value.replace(" ", "").split(),
				self.folders_include.value.replace(" ", "").split(), 
				self.folders_exclude.value.replace(" ", "").split(), 
				self.version.value if self.version.value != "" else 32
				)
			await Interaction.response.send_message(f"{Emojis.deta_rack} Кастомный шаблон датапака", file=discord.File(dp, filename="Custom datapack.zip"))
	
	class RP(discord.ui.Modal):
		def __init__(self):
			super().__init__(title=f"📁 Настройка ресурспака")
			self.custom_id="template:resourcepack"

		name = discord.ui.TextInput(
			required=False,
			label="Название",
			placeholder="Мой куртой ресурспак",
			max_length=64
		)
		namespaces = discord.ui.TextInput(
			required=False,
			label="Пространства имён",
			placeholder="my_rp, essential, ...",
			max_length=512
		)
		folders_include = discord.ui.TextInput(
			required=False,
			label="Включить папки",
			placeholder="models, шейдеры, enviroment, ...",
			max_length=512
		)
		folders_exclude = discord.ui.TextInput(
			required=False,
			label="Исключить папки",
			placeholder="models, шейдеры, enviroment, ...",
			max_length=512
		)
		version = discord.ui.TextInput(
			required=False,
			label="Версия",
			placeholder="Последняя/1.19.4/27",
			max_length=10
		)
		async def on_submit(self, Interaction: discord.Interaction):
			rp = PGenerator.resourcepack(
				self.name.value if self.name.value != "" else "repuksrack", 
				self.namespaces.value.replace(" ", "").split(),
				self.folders_include.value.replace(" ", "").split(), 
				self.folders_exclude.value.replace(" ", "").split(), 
				self.version.value if self.version.value != "" else 32
				)
			await Interaction.response.send_message(f"{Emojis.resource_rack} Кастомный шаблон ресурспака", file=discord.File(rp, filename="Custom resourcepack.zip"))

