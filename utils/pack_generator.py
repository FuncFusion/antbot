import discord

from utils.msg_utils import Emojis
from utils.packmcmeta import get_mcmeta_ver
from utils.validator import validate

import io
from string import ascii_lowercase, digits
from json import dumps
from zipfile import ZipFile, ZIP_DEFLATED
from Levenshtein import distance

class Templates:
	mcmeta = '{{\n\t"pack": {{\n\t\t"pack_format": {0},\n\t\t"description": "https://discord.gg/anthill-914772142300749854"\n\t}}\n}}'
	load_json = '{{\n\t"values": [\n\t\t"{0}:load"\n\t]\n}}'
	tick_json = '{{\n\t"values": [\n\t\t"{0}:tick"\n\t]\n}}'
	load = "say Это лоад функция"
	tick = "# Это тик функция"
	custom_model_data = '{{\n\t"parent": "item/generated",\n\t"textures": {{\n\t\t"layer0": "<путь к текстуре>"\n\t}},\n\t"overrides": [\n\t\t{{ "predicate": {{ "custom_model_data": {0} }}, "model": "item/cosmetics/eye_patch"}},\n\t]}}'


class PGenerator:
	legacy_dp_folders = {
		"advancements": ["адвансмент", "ачивки", "достижения"],
		"banner_pattern": ["баннер паттерн", "шаблон флага", "шаблон баннера"],
		"chat_type": ["чат тайп", "тип чата"],
		"damage_type": ["дэмедж тайп", "тип урона"],
		"dimension": ["дименшон", "измерение"],
		"dimension_type": ["дименшон тайп", "тип измерения"],
		"enchantment": ["энчантмент", "энчанты", "зачарования", "зачары"],
		"enchantment_provider": ["энчантмент провайдер", "провайдер энчантов", "почставщик зачарования", "зачары"],
		"functions": ["func", "функ", "функции"],
		"jukebox_song": ["джукбокс сонг", "песня проигрователя", "диск", "пластинка"],
		"loot_tables": ["лут тейблы", "таблицы лута", "таблицы добычи"],
		"painting_variant": ["пейнтинг вариант", "варианты картин", "вариации картин", "картины"],
		"predicates": ["предикетс", "предикаты"],
		"item_modifiers": ["айтем модифаеры", "модификаторы предметов"],
		"recipes": ["ресипис", "рецепты", "рецепты крафта"],
		"structures": ["стракчерс", "структуры", "данжи"],
		"tags": ["тэгс", "теги", "ярлыки"],
		"trim_material": ["трим материал", "материал шаблона"],
		"trim_pattern": ["трим паттерн", "кузнечный шаблон", "отделка брони"],
		"wolf_variant": ["волф вариант", "вариант волка"],
		"worldgen": ["ворлдген", "генерация", "генерация мира"]
		}
	dp_folders = {
		"advancement": ["адванцмент", "ачивки", "достижения"],
		"banner_pattern": ["баннер паттерн", "шаблон флага", "шаблон баннера"],
		"chat_type": ["чат тайп", "тип чата"],
		"damage_type": ["дэмедж тайп", "тип урона"],
		"dimension": ["дименшон", "измерение"],
		"dimension_type": ["дименшон тайп", "тип измерения"],
		"enchantment": ["энчантмент", "энчанты", "зачарования", "зачары"],
		"enchantment_provider": ["энчантмент провайдер", "провайдер энчантов", "почставщик зачарования", "зачары"],
		"function": ["func", "функ", "функции"],
		"jukebox_song": ["джукбокс сонг", "песня проигрователя", "диск", "пластинка"],
		"instrument": ["музыкальные инструменты", "инструменты", "штыекгьуте"],
		"loot_table": ["лут тейблы", "таблицы лута", "таблицы добычи"],
		"painting_variant": ["пейнтинг вариант", "варианты картин", "вариации картин", "картины"],
		"predicate": ["предикейтс", "предикаты"],
		"item_modifier": ["айтем модифиерс", "модификаторы предметов"],
		"recipe": ["ресипис", "рецепты", "рецепты крафта"],
		"structure": ["стракчерс", "структуры", "данжи"],
		"tags": ["тэгс", "теги", "ярлыки"],
		"trim_material": ["трим материал", "материал шаблона"],
		"trim_pattern": ["трим паттерн", "кузнечный шаблон", "отделка брони"],
		"wolf_variant": ["волф враинат", "вариант волка"],
		"worldgen": ["ворлдген", "генерация", "генерация мира"]
		}
	rp_folders = {
		"atlases": ["атласы"],
		"blockstates": ["блокстейтс", "блок стейты", "состояния блоков"],
		"font": ["фонт", "шрифт"],
		"lang": ["лэнг", "язык"],
		"models": ["моделс", "модели"],
		"particles": ["партиклс", "партиклы", "частицы"],
		"shaders": ["шейдерс", "шейдеры", "тёмная магия"],
		"texts": ["текстс", "текста", "строки"],
		"textures": ["тещурс", "текстуры"]
	}

	def validate_folders(folders, type, legacy=False):
		existing_fldrs = PGenerator.dp_folders if type == "dp" else PGenerator.rp_folders
		existing_fldrs = PGenerator.legacy_dp_folders if legacy and type == "dp" else existing_fldrs
		valid_folders = set()
		for folder in folders:
			valid_folder = validate(folder, existing_fldrs)
			if valid_folder != None:
				valid_folders.add(valid_folder)
		return list(valid_folders)
	
	def validate_namespaces(namespaces):
		valid_chars = ascii_lowercase + digits + "._-" 
		valid_namespaces = set()
		curr_nspc = ""
		for nspc in namespaces:
			curr_nspc = ''.join([char for char in nspc.lower() if char in valid_chars])
			if curr_nspc != "":
				valid_namespaces.add(curr_nspc)
		return list(valid_namespaces)
	
	def validate_version(version, type):
		version = version.replace(" ", "")
		if version.isnumeric():
			return int(version)
		else:
			cleaned_version = ''.join(filter(str.isdigit, version))
			try:
				major, *rest = cleaned_version
				minor, *patch = rest
				version = f"{major}.{minor}{'.'.join(patch)}"
			except:
				version = "latest"
			version = get_mcmeta_ver(type, version)
			return version

	def datapack(name="детарак", namespaces=["namespace"], folders_include=[], folders_exclude=[], version="latest"):
		# Validating stuff
		version = PGenerator.validate_version(version, "data_pack")
		legacy = version < 45
		folders_include = PGenerator.validate_folders(folders_include, "dp", legacy)
		folders_exclude = PGenerator.validate_folders(folders_exclude, "dp", legacy)
		namespaces = PGenerator.validate_namespaces(namespaces)
		main_namespace = "namespace" if namespaces == [] else namespaces[0]
		legacy_all_folders = list(PGenerator.legacy_dp_folders)
		all_folders = list(PGenerator.dp_folders)
		# Generating dp
		dp_f = io.BytesIO()
		with ZipFile(dp_f, "w") as dp:
			function = "functions" if legacy else "function"
			dp.writestr(f"{name}/pack.mcmeta", Templates.mcmeta.format(version))
			dp.writestr(f"{name}/data/minecraft/tags/{function}/load.json", Templates.load_json.format(main_namespace))
			dp.writestr(f"{name}/data/minecraft/tags/{function}/tick.json", Templates.tick_json.format(main_namespace))
			dp.writestr(f"{name}/data/{main_namespace}/{function}/load.mcfunction", Templates.load)
			dp.writestr(f"{name}/data/{main_namespace}/{function}/tick.mcfunction", Templates.tick)
			for namespace in namespaces:
				dp.mkdir(f"{name}/data/{namespace}")
			if folders_exclude == []:
				if folders_include == []:
					for folder in (all_folders if not legacy else legacy_all_folders):
						dp.mkdir(f"{name}/data/{main_namespace}/{folder[:]}")
				else:
					for folder in folders_include:
						dp.mkdir(f"{name}/data/{main_namespace}/{folder}")
		dp_f.seek(0)
		return dp_f
	
	def resourcepack(name="репуксрак", namespaces=[], folders_include=[], folders_exclude=[], version="latest"):
		# Validating stuff
		all_folders = ["atlases", "blockstates", "font", "lang", "models", "particles", "shaders", "texts", "textures"]
		folders_include = PGenerator.validate_folders(folders_include, "rp"); folders_include = folders_include if folders_include != [] else all_folders
		folders_exclude = PGenerator.validate_folders(folders_exclude, "rp")
		namespaces = PGenerator.validate_namespaces(namespaces)
		version = PGenerator.validate_version(version, "resource_pack")
		main_namespace = "namespace" if namespaces == [] else namespaces[0]
		# Generating rp
		rp_f = io.BytesIO()
		with ZipFile(rp_f, "w") as rp:
			rp.writestr(f"{name}/pack.mcmeta", Templates.mcmeta.format(version))
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
			label="Пространства имён (разделять пробелом)",
			placeholder="my_dp raycasts ...",
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
				self.name.value if self.name.value != "" else "detarack", 
				self.namespaces.value.split(),
				self.folders_include.value.split(), 
				self.folders_exclude.value.split(), 
				self.version.value if self.version.value != "" else str(get_mcmeta_ver())
				)
			await Interaction.response.send_message(f"## {Emojis.deta_rack} Кастомный шаблон датапака", 
				file=discord.File(dp, filename="Custom_datapack_(UNZIP).zip"))
	
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
			placeholder="my_rp essential ...",
			max_length=512
		)
		folders_include = discord.ui.TextInput(
			required=False,
			label="Включить папки",
			placeholder="models, шейдеры, environment, ...",
			max_length=512
		)
		folders_exclude = discord.ui.TextInput(
			required=False,
			label="Исключить папки",
			placeholder="models, шейдеры, environment, ...",
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
				self.namespaces.value.split(),
				self.folders_include.value.split(), 
				self.folders_exclude.value.split(), 
				self.version.value if self.version.value != "" else str(get_mcmeta_ver("resource_pack"))
				)
			await Interaction.response.send_message(f"## {Emojis.resource_rack} Кастомный шаблон ресурспака", 
				file=discord.File(rp, filename="Custom_resourcepack_(UNZIP).zip"))
