import discord
from discord import ui
from discord.ext import commands
from discord.utils import MISSING

from asyncio import create_task

from settings import (
    IVEN_GENERALS_CHANNEL_ID, IVEN_CHAT_ID, 
    IVEN_GENERAL_ROLE, IVEN_PARTICIPANT_ROLE,
    IVEN_REJECTED_ROLE, IVEN_PENDING_ROLE, GUILD,
    ADMIN_ROLE
)
from utils import Emojis, no_ping, handle_errors


general_role = None
participant_role = None
pending_role = None
rejected_role = None


class IvenRequests(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        create_task(self.setup_roles(bot))
    
    async def setup_roles(self, bot: commands.Bot):
        global general_role, participant_role, pending_role, rejected_role
        guild = await bot.fetch_guild(GUILD)
        general_role = await guild.fetch_role(IVEN_GENERAL_ROLE)
        participant_role = await guild.fetch_role(IVEN_PARTICIPANT_ROLE)
        pending_role = await guild.fetch_role(IVEN_PENDING_ROLE)
        rejected_role = await guild.fetch_role(IVEN_REJECTED_ROLE)

    @commands.has_permissions(administrator=True)
    @commands.command(name="iven_reqs_init")
    async def iven_reqs_init(self, ctx: commands.Context):
        await ctx.send(view=IvenRequestMessageLayout(), allowed_mentions=no_ping)
    
    @commands.has_any_role(ADMIN_ROLE, IVEN_GENERAL_ROLE)
    @commands.hybrid_command(
        name="iven-ban",
        aliases=["iven_ban", "iban", "шифт", "шмут_ифт", "ибан", "ивень_бан"],
        description="Ограничивает доступ к ивню",
        usage="`/iven-ban <участник>`",
        help=""
    )
    async def iven_ban(self, ctx: commands.Context, user: discord.Member):
        if user.get_role(IVEN_GENERAL_ROLE) != None:
            raise Exception("user is general")
        try:
            await user.add_roles(rejected_role)
        except:
            raise Exception("already rejected")
        try:
            await user.remove_roles(participant_role)
        except:pass
        await ctx.send(f"{Emojis.ban} {user.mention} забанен на ивне")

    @iven_ban.error
    async def iven_ban_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "contains": "already rejected",
                "msg": "Участник уже забанен"
            },
            {
                "contains": "user is general",
                "msg": "Не туда воюешь э"
            }
        ])
    
    @commands.has_any_role(ADMIN_ROLE, IVEN_GENERAL_ROLE)
    @commands.hybrid_command(
        name="iven-unban",
        aliases=["iven_unban", "iunban", "шгтифт", "шмут_гтифт", "иразбан", "ивень_разбан", "ивень_анбан"],
        description="Убирает ограничение на ивень",
        uasge="`/iven-unban <участник>`",
        help=""
    )
    async def iven_unban(self, ctx: commands.Context, user: discord.Member):
        if user.get_role(IVEN_REJECTED_ROLE) == None:
            raise Exception("not banned")
        await user.remove_roles(rejected_role)
        await ctx.send(f"{Emojis.ban} {user.mention} разбанен на ивне", allowed_mentions=no_ping)
        
    @iven_unban.error
    async def iven_unban_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "contains": "not banned",
                "msg": "Участник не забанен на ивне"
            }
        ])


class IvenRequestMessageLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
    
    textie = ui.TextDisplay(
        "**Ивень** - *это военный стратегически-тактический ивент с множеством уникальных механик,"
        " проводящийся в Майнкрафте.*\nДве противоборствующие команды сражаются за город. *Цель: "
        "уничтожить весь личный состав противника.*\n"
        "На вооружении у солдат имеются различные виды пушек: от дробовиков и снайперских винтовок "
        "до РПГ и ПЗРК, а также грузовики, мотоциклы, РСЗО, грузовые и боевые вертолеты и многое"
        " другое.\n"
        "У игроков есть простор для хитрых решений, таких как десант в тыл врага, установка "
        "блокпостов, подрыв мостов, дорог и многих других.\n"
        "В конце игры в город сбрасывается воздушный груз с модулями наведения авиабомб для "
        "окончательного закрепления стратегического доминирования над врагом."
    )
    sep = ui.Separator()
    ar = ui.ActionRow()

    @ar.button(label="Отправить заявку", emoji="📩", custom_id="iven:request_button")
    async def create_request(self, ctx: discord.Interaction, _):
        if ctx.user.get_role(IVEN_PARTICIPANT_ROLE) != None:
            await ctx.response.send_message(f"{Emojis.check} Ваша заявка была принята ранее", ephemeral=True)
        elif ctx.user.get_role(IVEN_REJECTED_ROLE) != None:
            await ctx.response.send_message(f"{Emojis.cross} Ваша заявка была отклонена ранее", ephemeral=True)
        elif ctx.user.get_role(IVEN_PENDING_ROLE) != None:
            await ctx.response.send_message(f"{Emojis.timeline_file} Ваша заявка на рассмотрении", ephemeral=True)
        else:
            await ctx.response.send_modal(IvenRequestForm())


class IvenRequestForm(ui.Modal):
    def __init__(self):
        super().__init__(title="Заявка на ивень", timeout=None, custom_id="iven:request_form")
    
    nick = ui.TextInput(
        label="Никнейм в майнкрафте",
        placeholder="saygex123",
        max_length=16
    )
    source = ui.TextInput(
        label="Откуда/от кого узнали об ивне",
        placeholder="Меня пригласил Х / Видел нарезку"
    )

    async def on_submit(self, ctx: discord.Interaction):
        generals_channel = await ctx.guild.fetch_channel(IVEN_GENERALS_CHANNEL_ID)
        await generals_channel.send(
            view=IvenDossier(ctx.user, self.children[0].value, self.children[1].value),
            allowed_mentions=no_ping
        )
        await ctx.response.send_message(f"{Emojis.check} Ваша заявка отправлена на проверку", ephemeral=True)
        await ctx.user.add_roles(pending_role)


class IvenDossier(ui.LayoutView):
    def __init__(
            self, 
            user: discord.Member=None, 
            nick: str=None, 
            source: str=None,
        ):
        super().__init__(timeout=None)
        if user == None:return

        self.add_item(_DossierCuntainer(user, nick, source))
    
class _DossierCuntainer(ui.Container):
    def __init__(
        self, 
        user: discord.Member=None, 
        nick: str=None, 
        source: str=None,
    ):
        super().__init__()
        self.user = user
        self.nick = nick
        self.source = source

        self.add_item(ui.Section(
            f"# {Emojis.user} Личное дело {user.mention}\n"
            f"**Ник**: {nick}\n"
            f"**Как узнал об ивне**: {source}",
            accessory=ui.Thumbnail(user.display_avatar.url)
        ))

        self.add_item(ui.Separator())
        self.add_item(ui.ActionRow())
        ar: ui.ActionRow = self.children[-1]

        accept_button = ui.Button(label="Принять", emoji=Emojis.check, custom_id="iven:accept_button")
        accept_button.callback = self.accept
        ar.add_item(accept_button)

        reject_button = ui.Button(label="Отклонить", emoji=Emojis.cross, custom_id="iven:reject_button")
        reject_button.callback = self.reject
        ar.add_item(reject_button)

    async def accept(self, ctx: discord.Interaction):
        await ctx.response.edit_message(view=IvenDossierVerdict(self.user, self.nick, self.source, True, ctx.user))
        await self.user.send(
            f"{Emojis.check} Ваша заявка на ивень была принята! Теперь вам доступен <#{IVEN_CHAT_ID}>"
        )
        await self.user.add_roles(participant_role, reason="Принят на ивень")
        await self.user.remove_roles(pending_role)
    
    async def reject(self, ctx: discord.Interaction):
        await ctx.response.edit_message(view=IvenDossierVerdict(self.user, self.nick, self.source, False, ctx.user))
        await self.user.send(
            f"{Emojis.cross} Ваша заявка на ивень отклонена"
        )
        await self.user.add_roles(rejected_role, reason="Не пригоден")
        await self.user.remove_roles(pending_role)


class IvenDossierVerdict(ui.LayoutView):
    def __init__(
            self, 
            user: discord.Member=None, 
            nick: str=None, 
            source: str=None, 
            accepted: bool = MISSING, 
            verdicter: discord.Member = MISSING
        ):
        super().__init__(timeout=None)
        if user == None:return
        
        self.add_item(ui.Container())
        cuntainer: ui.Container = self.children[-1]
        cuntainer.add_item(
            ui.Section(
                f"# {Emojis.user} Личное дело {user.mention}\n"
                f"**Ник**: {nick}\n"
                f"**Как узнал об ивне**: {source}",
                accessory=ui.Thumbnail(user.display_avatar.url)
            )
        )
        cuntainer.add_item(ui.Separator())
        cuntainer.add_item(ui.ActionRow())
        ar: ui.ActionRow = cuntainer.children[-1]

        if accepted:
            ar.add_item(ui.Button(
                style=discord.ButtonStyle.green, 
                label=f"Игрок принят {verdicter.display_name}",
                emoji=Emojis.check,
                disabled=True
            ))
        else:
            ar.add_item(ui.Button(
                style=discord.ButtonStyle.red, 
                label=f"Игрок отклонен {verdicter.display_name}",
                emoji=Emojis.cross,
                disabled=True
            ))
