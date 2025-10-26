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
        ticket_message += f"## {Emojis.worldgen_file} Версия майнкрафта\n`{data.get('mc_version')}`\n"
        ticket_message += f"## {Emojis.jar} Моды\n`{data.get('mod_list')}`\n"
        ticket_message += f"## {Emojis.loot_table_file} Конечная цель\n{data.get('end_goal')}\n"
        if description:=data.get("description"):
            ticket_message += f"## {Emojis.txt} Подробности\n{description}\n"

        help_forum = await ctx.guild.fetch_channel(HELP_FORUM_ID)
        msg = await fake_send(
            ctx.user, 
            help_forum, 
            view=LazyLayout(ui.TextDisplay(ticket_message), container=False),
            thread_name=data.get("thread_name"),
            allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False)
        )
        await msg.channel.send(view=StarterMessageLayout())


class SearchFirstCheck(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
    
    q = ui.TextDisplay(
        f"## {Emojis.question_mark} Потратили ли вы хотя бы "
        f"3 минуты на поиск похожих проблем в <#{HELP_FORUM_ID}>?"
    )
    ar = ui.ActionRow()

    @ar.button(label="Да", emoji=Emojis.check, custom_id="tickets:search_first_check:yes")
    async def yes(self, ctx: discord.Interaction, _):
        await ctx.response.send_modal(TicketModal())
    
    @ar.button(label="Нет", emoji=Emojis.cross, custom_id="tickets:search_first_check:no")
    async def no(self, ctx: discord.Interaction, _):
        await ctx.response.send_message(
            f"{Emojis.exclamation_mark} Сначала, поищите похожие "
            f"посты в <#{HELP_FORUM_ID}>! Это поможет сэкономить "
            "время и вам, и тем, кто помогает в ветках.",
            ephemeral=True
        )


class CreateTicketMessage(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
    
    class Cuntainer(ui.Container):
        textie = ui.TextDisplay(
            f"# {Emojis.pin} Добро пожаловать в помощь!\n"
            f"Здесь вы можете создать ветку в канале <#{HELP_FORUM_ID}> через систему тикетов.\n"
            f"# {Emojis.exclamation_mark} Перед созданием тикета\n"
            f"- Потратьте пару минут на поиск похожих проблем в <#{HELP_FORUM_ID}>.\n"
            "- Используйте команду </faqs:1200929455468724294> в канале https://discord.com/channels/914772142300749854/916788471480348743, "
            "чтоб посмотреть на частозадаваемые вопросы и ответы на них, например, факьюшка `?макросы` покажет гайд по макросам.\n"
            "- Чем больше информации вы предоставите о вашей проблеме, тем больше шансов на быструю и эффективную помощь.\n"
            f"# {Emojis.check} Для того, чтобы создать тикет, нажмите на кнопку ниже и следуйте инструкциям."
        )
        sep = ui.Separator()
        ar = ui.ActionRow()
    
        @ar.button(label="Создать тикет", emoji=Emojis.tags_file, custom_id="tickets:create_button")
        async def create_ticket(self, ctx: discord.Interaction, _):
            await ctx.response.send_message(view=SearchFirstCheck(), ephemeral=True)

    cuntainer = Cuntainer()


class TicketModal(ui.Modal):
    def __init__(self):
        super().__init__(title="Создание тикета", timeout=None, custom_id="tickets:create_ticket")
    
    thread_name = ui.TextInput(
        label="Название ветки",
        placeholder="Суть проблемы в одном предложении",
        max_length=100
    )

    end_goal = ui.TextInput(
        label="Что вы пытаетесь сделать в итоге?",
        placeholder="Опишите вашу изначальную задачу, а не ваш способ её решения",
        style=discord.TextStyle.long,
        max_length=512
    )

    mc_version = ui.TextInput(
        label="Версия майнкрафта и модлоадер",
        placeholder="Примеры: \"1.21.8 фабрик\", \"1.16.5 ванилла\"",
        max_length=20
    )

    mod_list = ui.TextInput(
        label="Список модов",
        placeholder="Примеры: \"ванилла\",\"оптифайн, ...\",\"скину скрин в ветке\"",
        style=discord.TextStyle.long,
        max_length=128
    )

    description = ui.TextInput(
        label="Подробное описание проблемы",
        placeholder="Что вы пытались сделать? Что произошло на самом деле? Опишите как можно более подробно.",
        required=False,
        style=discord.TextStyle.long,
        max_length=3072
    )

    async def on_submit(self, ctx: discord.Interaction):
        input_names = ("thread_name", "end_goal" 
            "mc_version", "mod_list", "description")
        
        await ctx.response.send_message(f"{Emojis.check} Пост был успешно создан в <#{HELP_FORUM_ID}>", ephemeral=True)
        await Tickets.create_ticket(ctx, {name:child.value for name, child in zip(input_names, self.children)})

