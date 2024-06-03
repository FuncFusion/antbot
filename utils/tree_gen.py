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
        "bbmodel": "<:bbmodel:1186764426376904714>"
    },
    "names": {
        "tick.json": "<:tickjson:1188838117940133930>",
        "load.json": "<:loadjson:1188838120712577174>",
        "sounds.json": "<:sounds_json:1142347091759353866>"
    },
    "open_folders": {
        "data": "<:data_open:1142345183367802971>",
        "advancement": "<:advancements:1142345174580740096>",
        "chat_type": "<:chat_type:1142345176921145435>",
        "damage_type": "<:damage_type:1142345178766659614>",
        "dimension": "<:dimension:1142928197168668752>",
        "dimension_type": "<:dimension_type:1143112349214068796>",
        "enchantment": "<:enchantment:1246812751938977915>",
        "enchantment_provider": "<:enchantment:1246812751938977915>",
        "function": "<:functions:1142345196642775090>",
        "jukebox_song": "<:jukebox_song:1246812914221060178>",
        "loot_table": "<:loot_tables:1142345293170491472>",
        "item_modififer": "<:item_modifiers:1142345199700414564>",
        "painting_variant": "<:painting_variant:1246812947083432026>",
        "predicate": "<:predicates:1142345430139666524>",
        "recipe": "<:recipes:1188841592715489361>",
        "structure": "<:structures:1142345436942827550>",
        "tags": "<:tags:1142345438654124033>",
        "trim_material": "<:trim_material:1142893110616150116>",
        "trim_pattern": "<:trim_pattern:1142893113594093660>",
        "worlgen": "<:worldgen:1142345441523019796>",
        "wolf_variant": "<:wolf_variant:1246817007161180232>",

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
        "banner_pattern": "<:banner_pattern:1246812899192737862>",
        "chat_type": "<:chat_type_file:1188838139700195348>",
        "damage_type": "<:damage_type_file:1188838136957112420>",
        "dimension": "<:dimension_file:1188838135300366336>",
        "dimension_type": "<:dimension_type_file:1188838133857534002>",
        "enchantment": "<:enchantment:1246812661866561536>",
        "enchantment_provider": "<:enchantment:1246812661866561536>",
        "jukebox_song": "<:jukebox_song:1246812929215430757>",
        "item_modifier": "<:item_modifier:1188838125565382728>",
        "recipe": "<:recipe:1188838131299004466>",
        "painting_variant": "<:painting:1142345422233423942>",
        "predicate": "<:predicate:1188838122633576488>",
        "trim_pattern": "<:trim_pattern_file:1188838127272464394>",
        "trim_material": "<:trim_material_file:1188838129495449671>",
        "wolf_variant": "<:wolf:1246816990669312011>",

        "models": "<:bbmodel:1186764426376904714>"
    }
}
registries = ["banner_pattern", "chat_type", "damage_type", "dimension", "dimension_type", "enchantment", "enchantment_provider", 
              "jukebox_song", "painting_variant", "item_modififer", "recipe",  "trim_materal", "trim_pattern", "wolf_variant",
              "worldgen", "models"]

def generate_tree(folders: str):
    folders = folders.split("\n")
    tree = ""
    curr_folder = ""
    file_ext = ""
    for idx, item in enumerate(folders):
        name = item.lstrip()
        if idx == len(folders)-1:
            break
        if "." in item:
            file_ext = item.split(".")[-1]
            if file_ext in icons["files"]:
                curr_icon = icons["files"][file_ext]
            else:
                curr_icon = icons["misc"]
            if file_ext == "json" and curr_folder in registries:
                curr_icon = icons["jsons"][curr_folder]
            if name in icons["names"]:
                curr_icon = icons["names"][name]
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
                    curr_icon = icons["namespace"]
                else:
                    curr_icon = icons["folder"]
            curr_folder = name
        if file_ext in ["mcf", "tmcf", "lmcf"]:
            formatted_name = name.replace(file_ext, "mcfunction")
        else:
            formatted_name = name
        tree += f"{'\u3000' * len(item.replace(name, ""))}⎿{curr_icon}`{formatted_name}`\n"
    return tree
