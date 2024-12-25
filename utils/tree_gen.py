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
		"advancement": e.advancement,
		"banner_pattern": e.banner_pattern,
		"chat_type": e.chat_type,
		"damage_type": e.damage_type,
		"datapacks": e.datapacks_open,
		"dimension": e.dimension,
		"dimension_type": e.dimension_type,
		"enchantment": e.enchantment,
		"enchantment_provider": e.enchantment,
		"function": e.function,
		"jukebox_song": e.sounds,
		"loot_table": e.loot_table,
		"instrument": e.instrument,
		"item_modifier": e.item_modifier,
		"painting_variant": e.painting_variant,
		"predicate": e.predicate,
		"recipe": e.recipe,
		"structure": e.structure,
		"tags": e.tags,
		"trial_spawner": e.trial_spawner,
		"trim_material": e.trim_material,
		"trim_pattern": e.trim_pattern,
		"worldgen": e.worldgen,
		"wolf_variant": e.wolf_variant,

		"advancements": e.advancement,
		"functions": e.function,
		"loot_tables": e.loot_table,
		"predicates": e.predicate,
		"item_modifiers": e.item_modifier,
		"recipes": e.recipe,
		"structures": e.structure,

		"assets": e.assets_open,
		"atlases": e.atlases,
		"blockstates": e.blockstates,
		"equipment": e.equipment,
		"font": e.font,
		"items": e.items,
		"lang": e.lang,
		"models": e.models,
		"particles": e.particles,
		"post_effects": e.shaders,
		"textures": e.textures,
		"texts": e.texts,
		"shaders": e.shaders,
		"sounds": e.sounds
	},
	"jsons": {
		"advancement": e.advancement,
		"banner_pattern": e.banner_pattern,
		"chat_type": e.chat_type,
		"damage_type": e.damage_type,
		"dimension": e.dimension,
		"dimension_type": e.dimension_type,
		"enchantment": e.enchantment,
		"enchantment_provider": e.enchantment,
		"jukebox_song": e.ogg,
		"instrument": e.instrument,
		"item_modifier": e.item_modifier,
		"recipe": e.recipe,
		"painting_variant": e.painting_variant,
		"predicate": e.predicate,
		"trial_spawner": e.trial_spawner,
		"trim_pattern": e.trim_pattern,
		"trim_material": e.trim_material,
		"wolf_variant": e.wolf_variant,
		"loot_table": e.loot_table,

		"advancements": e.advancement,
		"item_modifiers": e.item_modifier,
		"loot_tables": e.loot_table,
		"predicates": e.predicate,
		"recipes": e.recipe,

		"atlases": e.atlases,
		"blockstates": e.blockstates,
		"equipment": e.equipment,
		"items": e.items,
		"lang": e.lang_file,
		"models": e.bbmodel,
		"particles": e.particles,
		"post_effects": e.shader_triangle,
		"shaders": e.shader_triangle,
	}
}
registries = [
	"advancement", "banner_pattern", "chat_type", "damage_type", "dimension", "dimension_type", 
	"enchantment", "enchantment_provider", "jukebox_song", "instrument", "painting_variant", 
	"predicate", "item_modifier", "recipe", "trial_spawner", "trim_material", "trim_pattern", 
	"wolf_variant", "loot_table",
	"advancements", "predicates", "item_modifiers", "recipes", "loot_tables",

	"atlases", "blockstates", "equipment", "items", "lang", "models", "particles", "post_effects", 
	"shaders",
	]
