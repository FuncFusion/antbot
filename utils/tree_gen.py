from utils.msg_utils import Emojis as e

def generate_tree(folders: str):
	folders = folders.split("\n")
	tree = ""
	file_ext = ""
	folder_history = [""]
	for idx, item in enumerate(folders):
		name = item.lstrip()
		if idx == len(folders)-1:
			indent_difference = 0
			if item == "":break
		else:
			indent_difference = (len(next_item:=folders[idx+1]) - len(next_item.lstrip())) - (len(item.replace(name, "")))
		if "." in item or name in icons["names"]:
			file_ext = item.split(".")[-1]
			if name in icons["names"]:
				curr_icon = icons["names"][name]
			elif file_ext == "json" and (last_register:=[folder for folder in folder_history if folder in registries]):
				curr_icon = icons["jsons"][last_register[-1]]
			elif file_ext in icons["files"]:
				curr_icon = icons["files"][file_ext]
			else:
				curr_icon = icons["misc"]
		else:
			if indent_difference > 0:
				if name in icons["open_folders"]:
					curr_icon = icons["open_folders"][name]
				elif folder_history != [] and folder_history[-1] in ["data", "assets"]:
					curr_icon = icons["open_namespace"]
				else:
					curr_icon = icons["open_folder"]
				folder_history.append(name)
			else:
				if folder_history != [] and folder_history[-1] in ["data", "assets"]:
					curr_icon = icons["namespace"]
				else:
					curr_icon = icons["folder"]
		if indent_difference < 0:
			for i in range(indent_difference * -1):
				try:
					folder_history.pop(-1)
				except:pass
		if file_ext in ["mcf", "tmcf", "lmcf"]:
			formatted_name = name.replace(file_ext, "mcfunction")
		else:
			formatted_name = name
		indent = "\u3000" * abs(len(item.replace(name, "")) - (1 if name != item else 0))
		tree += f"{indent}{'\u23bf' if name != item else ""}{curr_icon}`{formatted_name}`\n"
	return tree[:-1]

icons = {
	"folder": e.folder,
	"open_folder": e.folder_open,
	"namespace": e.namespace,
	"open_namespace": e.namespace_open,
	"misc": e.misc,
	"files": {
		"mcfunction": e.mcf,
		"mcf": e.mcf,
		"tmcf": e.mcf_tick,
		"lmcf": e.mcf_load,
		"nbt": e.nbt,
		"png": e.image,
		"mcmeta": e.pack_mcmeta,
		"json": e.json,
		"vsh": e.vsh,
		"fsh": e.fsh,
		"glsl": e.glsl,
		"ogg": e.ogg,
		"bbmodel": e.bbmodel,
		"py": e.python,
		"ttf": e.ttf,
		"txt": e.txt,
		"nbt": e.nbt
	},
	"names": {
		"...": "",
		"tick.json": e.tick_json,
		"load.json": e.load_json,
		"sounds.json": e.sounds_json,
		"LICENSE": e.license,
		"LICENSE.md": e.license,
		"LICENSE.txt": e.license,
		"say.gex": e.bth123
	},
	"open_folders": {
		"data": e.data_open,
		"advancement": e.advancements_open,
		"banner_pattern": e.banner_pattern_open,
		"chat_type": e.chat_type_open,
		"damage_type": e.damage_type_open,
		"datapacks": e.datapacks_open,
		"dimension": e.dimension_open,
		"dimension_type": e.dimension_type_open,
		"enchantment": e.enchantment_open,
		"enchantment_provider": e.enchantment_open,
		"function": e.functions_open,
		"jukebox_song": e.sounds_open,
		"loot_table": e.loot_tables_open,
		"item_modifier": e.item_modifiers_open,
		"painting_variant": e.painting_variant_open,
		"predicate": e.predicates_open,
		"recipe": e.recipes_open,
		"structure": e.structures_open,
		"tags": e.tags_open,
		"trim_material": e.trim_material_open,
		"trim_pattern": e.trim_pattern_open,
		"worldgen": e.worldgen_open,
		"wolf_variant": e.wolf_variant_open,

		"advancements": e.advancements_open,
		"functions": e.functions_open,
		"loot_tables": e.loot_tables_open,
		"predicates": e.predicates_open,
		"item_modifiers": e.item_modifiers_open,
		"recipes": e.recipes_open,
		"structures": e.structures_open,

		"assets": e.assets_open,
		"atlases": e.atlases_open,
		"blockstates": e.blockstates_open,
		"font": e.font_open,
		"lang": e.lang_open,
		"models": e.models_open,
		"particles": e.particles_open,
		"textures": e.textures_open,
		"shaders": e.shaders_open,
		"sounds": e.sounds_open
	},
	"jsons": {
		"advancement": e.advancements_json,
		"advancements": e.advancements_json,
		"banner_pattern": e.banner_pattern_json,
		"chat_type": e.chat_type_json,
		"damage_type": e.damage_type_json,
		"dimension": e.dimension_json,
		"dimension_type": e.dimension_type_json,
		"enchantment": e.enchantment_json,
		"enchantment_provider": e.enchantment_json,
		"jukebox_song": e.ogg,
		"item_modifier": e.item_modifiers_json,
		"item_modifiers": e.item_modifiers_json,
		"recipe": e.recipes_json,
		"recipes": e.recipes_json,
		"painting_variant": e.painting_variant_json,
		"predicate": e.predicates_json,
		"predicates": e.predicates_json,
		"trim_pattern": e.trim_pattern_json,
		"trim_material": e.trim_material_json,
		"wolf_variant": e.wolf_variant_json,
		"lang": e.lang,
		"models": e.bbmodel,
		"atlases": e.atlases_open,
		"blockstates": e.blockstates_json,
		"particles": e.particles_json,
		"loot_table": e.loot_tables_json,
		"loot_tables": e.loot_tables_json
	}
}
registries = ["advancement", "banner_pattern", "chat_type", "damage_type", "dimension", "dimension_type", 
	"enchantment", "enchantment_provider", "jukebox_song", "painting_variant", "predicate", 
	"item_modifier", "recipe", "trim_material", "trim_pattern", "wolf_variant", "lang", "models",
	"atlases", "blockstates", "particles", "loot_table","loot_tables",
	"advancements", "predicates", "item_modifiers", "recipes"
	]
