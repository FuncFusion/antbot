import discord
from discord.ext import commands

from utils.msg_utils import Emojis
from utils.validator import validate

from cogs.mc.pack_generator import Modals


async def template_command(ctx, template: str="datapack", type: str="basic"):
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
            await ctx.send(f"{pack_ctx[template]["emoji"]} Расширенный шаблон {pack_ctx[template]["accusative"]}", 
            file=discord.File(pack, filename=f"Extended_{template}_(UNZIP).zip"))
    elif type == "basic":
        with open(f"assets/templates/Basic {template}.zip", "rb") as pack:
            await ctx.send(f"{pack_ctx[template]["emoji"]} Базовый шаблон {pack_ctx[template]["accusative"]}", 
            file=discord.File(pack, filename=f"Basic_{template}_(UNZIP).zip"))
