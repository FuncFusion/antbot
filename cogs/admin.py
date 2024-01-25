import discord
from discord.ext import commands
from discord import app_commands



class AdminCommands(commands.Cog):
    def __init__(self, bot):

        @bot.hybrid_command(aliases=["offline", "off", "disconnect", "дисконнект", "отключись", "выкл", "выключись", "оффлайн", "офф", "вшысщттусе", "щаадшту", "щаа", "ыргевщцт"],
                            description="Отключает бота.")
        async def shutdown(ctx):
            await ctx.send("Отключаюсь...")
            await bot.close()

        @bot.hybrid_command(aliases=["on"],
                            description="Меняет статус бота на \"В сети\".")
        async def online(ctx):
            await ctx.send("Теперь мой статус - `В сети`.")
            await bot.change_presence(status=discord.Status.online)

        @bot.hybrid_command(aliases=["afk"],
                            description="Меняет статус бота на \"Отошёл\".")
        async def idle(ctx):
            await ctx.send("Теперь мой статус - `Отошёл`.")
            await bot.change_presence(status=discord.Status.idle)

        @bot.hybrid_command(aliases=["dnd"],
                            description="Меняет статус бота на \"Не беспокоить\".")
        async def donotdisturb(ctx):
            await ctx.send("Теперь мой статус - `Не беспокоить`.")
            await bot.change_presence(status=discord.Status.do_not_disturb)

        @bot.hybrid_command(aliases=["invis"],
                            description="Меняет статус бота на \"Невидимка\".")
        async def invisible(ctx):
            await ctx.send("Теперь мой статус - `Невидимка`.")
            await bot.change_presence(status=discord.Status.invisible)