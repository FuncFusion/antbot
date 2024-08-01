def generate_tree(folders: str):
	folders = folders.split("\n")
	tree = ""
	file_ext = ""
	folder_history = [""]
	for idx, item in enumerate(folders):
		if idx == len(folders)-1:
			break
		name = item.lstrip()
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
	return tree

icons = {
	"folder": "<:folder:1142345186949734482>",
	"open_folder": "<:folder_open:1142345194805669918>",
	"namespace": "<:namespace:1188839155170545705>",
	"open_namespace": "<:namespace_open:1188839157829742723>",
	"misc": "<:misc:1142345412938834022>",
	"files": {
		"mcfunction": "<:mcfunction:1142345406106312754>",
		"mcf": "<:mcfunction:1142345406106312754>",
		"tmcf": "<:mcfunction_tick:1142345408459321425>",
		"lmcf": "<:mcfunction_load:1142345404403425341>",
		"nbt": "<:nbt:1142345418949279753>",
		"png": "<:painting:1142345422233423942>",
		"mcmeta": "<:pack_mcmeta:1142345410380304414>",
		"json": "<:json:1142345204402233434>",
		"vsh": "<:vsh:1142347174223552543>",
		"fsh": "<:fsh:1142347278812725258>",
		"glsl": "<:glsl:1142347436740849745>",
		"ogg": "<:ogg:1142918898157629620>",
		"bbmodel": "<:bbmodel:1186764426376904714>",
		"py": "<:python:1186764496270794893>"
	},
	"names": {
		"...": "",
		"tick.json": "<:tickjson:1188838117940133930>",
		"load.json": "<:loadjson:1188838120712577174>",
		"sounds.json": "<:sounds_json:1142347091759353866>",
		"LICENSE": "<:license:1246813468108001392>",
		"LICENSE.md": "<:license:1246813468108001392>",
		"LICENSE.txt": "<:license:1246813468108001392>",
		"say.gex": "<:be_style_bth123:1096442989389291610>"
	},
	"open_folders": {
		"data": "<:data_open:1142345183367802971>",
		"advancement": "<:advancements:1142345174580740096>",
		"banner_pattern": "<:banner_pattern:1246812883170492436>",
		"chat_type": "<:chat_type:1142345176921145435>",
		"damage_type": "<:damage_type:1142345178766659614>",
		"datapacks": "<:datapacks:1186764442277527713>",
		"dimension": "<:dimension:1142928197168668752>",
		"dimension_type": "<:dimension_type:1143112349214068796>",
		"enchantment": "<:enchantment:1246812751938977915>",
		"enchantment_provider": "<:enchantment:1246812751938977915>",
		"function": "<:functions:1142345196642775090>",
		"jukebox_song": "<:jukebox_song:1246812914221060178>",
		"loot_table": "<:loot_tables:1142345293170491472>",
		"item_modifier": "<:item_modifiers:1142345199700414564>",
		"painting_variant": "<:painting_variant:1246812947083432026>",
		"predicate": "<:predicates:1142345430139666524>",
		"recipe": "<:recipes:1188841592715489361>",
		"structure": "<:structures:1142345436942827550>",
		"tags": "<:tags:1142345438654124033>",
		"trim_material": "<:trim_material:1142893110616150116>",
		"trim_pattern": "<:trim_pattern:1142893113594093660>",
		"worldgen": "<:worldgen:1142345441523019796>",
		"wolf_variant": "<:wolf_variant:1246817007161180232>",

		"advancements": "<:advancements:1142345174580740096>",
		"functions": "<:functions:1142345196642775090>",
		"loot_tables": "<:loot_tables:1142345293170491472>",
		"predicates": "<:predicates:1142345430139666524>",
		"item_modifiers": "<:item_modifiers:1142345199700414564>",
		"recipes": "<:recipes:1188841592715489361>",
		"structures": "<:structures:1142345436942827550>",

		"assets": "<:assets_open:1142346941599064086>",
		"atlases": "<:atlases:1142347325436612619>",
		"blockstates": "<:blockstates:1142346756953231451>",
		"font": "<:font:1142346540392927262>",
		"lang": "<:lang:1142346828206047325>",
		"models": "<:models:1142346673469800479>",
		"particles": "<:particles:1142346351879925862>",
		"textures": "<:textures:1142347361893494876>",
		"shaders": "<:shaders:1142346604028899429>",
		"sounds": "<:sounds:1142347049568837742>"
	},
	"jsons": {
		"advancement": "<:advancement:1248200508318154813>",
		"advancements": "<:advancement:1248200508318154813>",
		"banner_pattern": "<:banner_pattern:1246812899192737862>",
		"chat_type": "<:chat_type_file:1188838139700195348>",
		"damage_type": "<:damage_type_file:1188838136957112420>",
		"dimension": "<:dimension_file:1188838135300366336>",
		"dimension_type": "<:dimension_type_file:1188838133857534002>",
		"enchantment": "<:enchantment:1246812661866561536>",
		"enchantment_provider": "<:enchantment:1246812661866561536>",
		"jukebox_song": "<:jukebox_song:1246812929215430757>",
		"item_modifier": "<:item_modifier:1188838125565382728>",
		"item_modifiers": "<:item_modifier:1188838125565382728>",
		"recipe": "<:recipe:1188838131299004466>",
		"recipes": "<:recipe:1188838131299004466>",
		"painting_variant": "<:painting:1142345422233423942>",
		"predicate": "<:predicate:1188838122633576488>",
		"predicates": "<:predicate:1188838122633576488>",
		"trim_pattern": "<:trim_pattern_file:1188838127272464394>",
		"trim_material": "<:trim_material_file:1188838129495449671>",
		"wolf_variant": "<:wolf:1246816990669312011>",
		"lang": "<:lang_file:1188838193559257258>",
		"models": "<:bbmodel:1186764426376904714>"
	}
}
registries = ["advancement", "banner_pattern", "chat_type", "damage_type", "dimension", "dimension_type", 
	"enchantment", "enchantment_provider", "jukebox_song", "painting_variant", "predicate", 
	"item_modifier", "recipe", "trim_material", "trim_pattern", "wolf_variant", "lang", "models",
	
	"advancements", "predicates", "item_modifiers", "recipes"
	]
