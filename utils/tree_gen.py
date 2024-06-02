icons = {
    "folder": "<:folder:1142345186949734482>",
    "open_folder": "<:folder_open:1142345194805669918>",
    "namespace": "<:namespace:1188839155170545705>",
    "open_namespace": "<:namespace_open:1188839157829742723>",
    "misc": "<:misc:1142345412938834022>",
    "open_folders": {
        "data": "<:data_open:1142345183367802971>",
        "advancement": "<:advancements:1142345174580740096>",
        "chat_type": "<:chat_type:1142345176921145435>",
        "damage_type": "<:damage_type:1142345178766659614>",
        "dimension": "<:dimension:1142928197168668752>",
        "dimension_type": "<:dimension_type:1143112349214068796>",
        "function": "<:functions:1142345196642775090>",
        "loot_table": "<:loot_tables:1142345293170491472>",
        "item_modififer": "<:item_modifiers:1142345199700414564>",
        "predicate": "<:predicates:1142345430139666524>",
        "recipe": "<:recipes:1188841592715489361>",
        "structure": "<:structures:1142345436942827550>",
        "tags": "<:tags:1142345438654124033>",
        "trim_material": "<:trim_material:1142893110616150116>",
        "trim_pattern": "<:trim_pattern:1142893113594093660>",
        "worlgen": "<:worldgen:1142345441523019796>",
    },
    "files": {
        "mcfunction": "<:mcfunction:1142345406106312754>",
        "mcf": "<:mcfunction:1142345406106312754>",
        "tmcf": "<:mcfunction_tick:1142345408459321425>",
        "lmcf": "<:mcfunction_load:1142345404403425341>",
        "nbt": "<:nbt:1142345418949279753>",
        "png": "<:painting:1142345422233423942>",
        "mcmeta": "<:pack_mcmeta:1142345410380304414>",
        "json": "<:json:1142345204402233434>"
    },
    "jsons": {
        "dimension": "<:dimension_file:1188838135300366336>",
        "dimension_type": "<:dimension_type_file:1188838133857534002>",
        "recipe": "<:recipe:1188838131299004466>",
        "damage_type": "<:damage_type_file:1188838136957112420>",
        "predicate": "<:predicate:1188838122633576488>",
        "chat_type": "<:chat_type_file:1188838139700195348>",
        "item_modifier": "<:item_modifier:1188838125565382728>",
        "trim_pattern": "<:trim_pattern_file:1188838127272464394>",
        "trim_material": "<:trim_material_file:1188838129495449671>",
    }
}
registries = ["advancement", "banner_pattern", "chat_type", "damage_type", "dimension", "dimension_type", "enchantment", "enchantment_provider", 
              "jukebox_song", "loot_table", "painting_variant", "recipe", "structure", "tags", "trim_materal", "trim_pattern", "wolf_variant", "worldgen"]

def generate_tree(folders: str):
    folders = folders.split("\n")
    tree = ""
    curr_folder = ""
    file_ext = ""
    for idx, item in enumerate(folders):
        name = item.lstrip()
        if "." in item:
            file_ext = item.split(".")[-1]
            if file_ext in icons["files"]:
                curr_icon = icons["files"][file_ext]
            else:
                curr_icon = icons["misc"]
            if file_ext == "json" and curr_folder in registries:
                curr_icon = icons["jsons"][curr_folder]
        else:
            if (len(next_line:=folders[idx+1]) - len(next_line.lstrip())) > (len(item) - len(item.lstrip())):
                if name in icons["open_folders"]:
                    curr_icon = icons["open_folders"][name]
                elif curr_folder in ["data", "assets"]:
                    curr_icon = icons["open_namespace"]
                else:
                    curr_icon = icons["open_folder"]
            else:
                if curr_folder in ["data", "assets"]:
                    curr_icon = icons["namesapce"]
                else:
                    curr_icon = icons["folder"]
            curr_folder = name
        if file_ext in ["mcf", "tmcf", "lmcf"]:
            formatted_name = name.replace(file_ext, "mcfunction")
        else:
            formatted_name = name
        tree += f"{'\u3000' * len(item.replace(name, ""))}⎿{curr_icon}`{formatted_name}`\n"
    return tree
