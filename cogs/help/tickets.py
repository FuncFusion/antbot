import discord
from discord import ui, SelectOption as SO
from discord.ext import commands

from settings import HELP_FORUM_ID
from cogs.help.starter_message import StarterMessageLayout
from utils import LazyLayout, Emojis, fake_send


class Tickets(commands.Cog):

    @commands.has_permissions(administrator=True)
    @commands.command(name="tickets_init")
    async def tickets_init(self, ctx: commands.Context):
        await ctx.send(view=CreateTicketMessage())
    

    async def create_ticket(ctx: discord.Interaction, data: dict):
        ticket_message = f"{ctx.user.mention}\n"
        
        # Filling out
        ticket_message += f"**{Emojis.worldgen_file} Версия майнкрафта**\n`{data.get('mc_version')}`\n"
        ticket_message += f"**{Emojis.jar} Моды**\n`{data.get('mod_list')}`\n"
        if description:=data.get("description"):
            ticket_message += f"**{Emojis.txt} Подробности**\n{description}\n"

        help_forum = await ctx.guild.fetch_channel(HELP_FORUM_ID)
        msg = await fake_send(
            ctx.user, 
            help_forum, 
            view=LazyLayout(ui.TextDisplay(ticket_message), container=False),
            thread_name=data.get("thread_name"),
            allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False)
        )
        await msg.channel.send(view=StarterMessageLayout())


class CreateTicketMessage(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
    
    class Cuntainer(ui.Container):
        textie = ui.TextDisplay("# Тикет ещекере\nну ты брат нажми кнопку, там интуитивно понятно")
        sep = ui.Separator()
        ar = ui.ActionRow()
    
        @ar.button(label="Создать тикет", emoji=Emojis.tags_file, custom_id="tickets:create_button")
        async def create_ticket(self, ctx: discord.Interaction, _):
            await ctx.response.send_modal(TicketModal())

    cuntainer = Cuntainer()


class TicketModal(ui.Modal):
    def __init__(self):
        super().__init__(title="\U0001f3f7 Создание тикета", timeout=None, custom_id="tickets:create_ticket")
    
    retard_test = ui.TextInput(
        label="Пробовали лы вы искать похожие посты в помощи",
        placeholder="Да | Нет",
        min_length=2,
        max_length=3
    )

    thread_name = ui.TextInput(
        label="Название ветки",
        placeholder="Краткое описание проблемы",
        max_length=100
    )

    mc_version = ui.TextInput(
        label="Версия майнкрафта и лоадер",
        placeholder="Например \"1.21.8 фабрик\", \"1.16.5 ванилла\"",
        max_length=20
    )

    mod_list = ui.TextInput(
        label="Список модов",
        placeholder="Например \"ванилла\", \"оптифайн, ...\", \"скину скрин в ветке\"",
        style=discord.TextStyle.long,
        max_length=128
    )

    description = ui.TextInput(
        label="Подробное описание проблемы",
        placeholder="Вот блинчик",
        required=False,
        style=discord.TextStyle.long,
        max_length=3072
    )

    async def on_submit(self, ctx: discord.Interaction):
        if not any(i in self.retard_test.value.lower() for i in ("да", "lf", "yes", "нуы")):
            await ctx.response.send_message(f"{Emojis.exclamation_mark} Сначала, "
                f"поищите похожие посты в <#{HELP_FORUM_ID}>! Это может сэкономить "
                "время и вам, и тем, кто помогает в ветках", 
                ephemeral=True
            )
            return

        input_names = ("retard_test", "thread_name", 
            "mc_version", "mod_list", "description")
        
        await ctx.response.send_message(f"{Emojis.check} Пост был успешно создан в <#{HELP_FORUM_ID}>", ephemeral=True)
        await Tickets.create_ticket(ctx, {name:child.value for name, child in zip(input_names, self.children)})

