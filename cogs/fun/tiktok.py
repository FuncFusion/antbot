import io

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import aiohttp

from utils import LazyLayout, Emojis, handle_errors, no_color, no_ping

class SeeImagesAR(ui.ActionRow):
    def __init__(self, urls: list[str], music: bytes):
        super().__init__()
        self.urls = urls
        self.music = music

    @ui.button(label="Смотреть изображения")
    async def see_images(self, ctx: discord.Interaction, button):
        await ctx.response.defer(ephemeral=True)

        music_file = discord.File(io.BytesIO(self.music), filename="music.mp3")

        view = TiktokImageView(self.urls, self.music)
        embed = discord.Embed(
            title=f"1/{len(self.urls)}",
            color=no_color
        )
        embed.set_image(url=self.urls[0])
        await ctx.followup.send(embed=embed, view=view, ephemeral=True, file=music_file)

class TiktokImageView(ui.View):
    def __init__(self, urls: list[str] = [], music: bytes = None, current: int = 0):
        super().__init__(timeout=None)
        self.urls = urls
        self.music = music
        self.current = current

        options = [
            discord.SelectOption(label=f"Изображение {i + 1}", value=str(i), default=(i == current))
            for i in range(len(urls))
        ]
        self.select = discord.ui.Select(
            placeholder="Выбери изображение...",
            options=options,
            custom_id="tiktok:select"
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

        if len(urls) == 1:
            self.clear_items()

    async def update_message(self, ctx: discord.Interaction):
        for option in self.select.options:
            option.default = (option.value == str(self.current))

        embed = discord.Embed(
            title=f"{self.current + 1}/{len(self.urls)}",
            color=no_color
        )
        embed.set_image(url=self.urls[self.current])
        await ctx.response.edit_message(embed=embed, view=self)

    async def select_callback(self, ctx: discord.Interaction):
        self.current = int(self.select.values[0])
        await self.update_message(ctx)

    @ui.button(label="<", custom_id="tiktok:left")
    async def prev(self, ctx: discord.Interaction, button: ui.Button):
        self.current = (self.current - 1) % len(self.urls)
        await self.update_message(ctx)

    @ui.button(label=">", custom_id="tiktok:right")
    async def next(self, ctx: discord.Interaction, button: ui.Button):
        self.current = (self.current + 1) % len(self.urls)
        await self.update_message(ctx)

class TikTokCommand(commands.Cog):
    @commands.hybrid_command(
        aliases=["тикток", "nbrnjr", "ешлещл", "tt", "ее", "тт", "nn"],
        description="Отправляет видео из TikTok по ссылке.",
        usage="`/tiktok <ссылка>`",
        help="### Пример:\n`/tiktok https://www.tiktok.com/@super.ant_/video/7306187825089629446`")
    @app_commands.describe(url="Ссылка на ролик в TikTok")

    async def tiktok(self, ctx: commands.Context, url: str):
        await ctx.defer()

        api_url = "https://www.tikwm.com/api/?url=" + url + "&hd=1"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    data = result.get("data", {})

                    if result.get("code") == 0 and not data.get("images") and data.get("hdplay"):
                        video = data.get("hdplay")
                        gex = LazyLayout(
                            ui.TextDisplay(url),
                            ui.MediaGallery(discord.MediaGalleryItem(media=video)),
                            container=False
                        )
                        await ctx.reply(view=gex, allowed_mentions=no_ping)
                    elif data.get("images"):
                        images = data.get("images")
                        music = data.get("music")
                        async with session.get(music) as m_resp:
                            if m_resp.status == 200:
                                music_bytes = await m_resp.read()
                        if len(images) > 1:
                            gex = LazyLayout(
                                ui.MediaGallery(discord.MediaGalleryItem(media=images[0])),
                                SeeImagesAR(images, music_bytes)
                            )
                            await ctx.reply(view=gex, allowed_mentions=no_ping)
                        else:
                            music_file = discord.File(io.BytesIO(music_bytes), filename="music.mp3")

                            view = TiktokImageView(images, music_bytes)
                            embed = discord.Embed(
                                color=no_color
                            )
                            embed.set_image(url=images[0])
                            await ctx.reply(embed=embed, view=view, file=music_file, allowed_mentions=no_ping)
                    else:
                        await ctx.reply(
                            Emojis.cross + "Ошибка! Не удалось скачать тикток."
                        )
                else:
                    await ctx.reply(f"Ошибка запроса! Код: {resp.status}")

    @tiktok.error
    async def tiktok_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "exception": commands.MissingRequiredArgument,
                "msg": "Введите ссылку на видео"
            }
        ])
