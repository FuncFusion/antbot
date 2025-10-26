import io

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import aiohttp

from utils import LazyLayout, Emojis, handle_errors, no_color, no_ping


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
                result = await resp.json()
                data = result.get("data", {})
                if resp.status != 200 or not (data.get("images") or data.get("hdplay")):
                    raise Exception("unable to get")
                

                if not data.get("images") and data.get("hdplay"):
                    video = data.get("hdplay")
                    await ctx.reply(
                        view=LazyLayout(
                            ui.TextDisplay(url),
                            ui.MediaGallery(discord.MediaGalleryItem(media=video)),
                            container=False
                        ),
                        allowed_mentions=no_ping
                    )

                elif data.get("images"):
                    images = data.get("images")
                    music_url = data.get("music")
                    if len(images) > 1:
                        await ctx.reply(
                            view=LazyLayout(
                                ui.MediaGallery(discord.MediaGalleryItem(media=images[0])),
                                SeeImagesAR(images, music_url)
                            ),
                            allowed_mentions=no_ping
                        )
                    else:
                        async with session.get(music_url) as m_resp:
                            music_bytes = await m_resp.read()
                        music_file = discord.File(io.BytesIO(music_bytes), filename="music.mp3")

                        embed = discord.Embed(
                            color=no_color
                        )
                        embed.set_image(url=images[0])
                        await ctx.reply(embed=embed, file=music_file, allowed_mentions=no_ping)


    @tiktok.error
    async def tiktok_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "exception": commands.MissingRequiredArgument,
                "msg": "Введите ссылку на видео"
            },
            {
                "contains": "unable to get",
                "msg": "Не удалось найти видео"
            }
        ])


class SeeImagesAR(ui.ActionRow):
    def __init__(self, images: list[str], music_url: str):
        super().__init__()
        self.images = images
        self.music_url = music_url

    @ui.button(label="Смотреть изображения")
    async def see_images(self, ctx: discord.Interaction, _):
        await ctx.response.defer(ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.music_url) as resp:
                music_bytes = await resp.read()
        music_file = discord.File(io.BytesIO(music_bytes), filename="music.mp3")

        view = TiktokImageView(self.images)
        embed = discord.Embed(
            title=f"1/{len(self.images)}",
            color=no_color
        )
        embed.set_image(url=self.images[0])
        await ctx.followup.send(embed=embed, view=view, ephemeral=True, file=music_file)


class TiktokImageView(ui.View):
    def __init__(self, urls: list[str] = [], current_slide: int = 0):
        super().__init__(timeout=None)
        self.urls = urls
        self.current_slide = current_slide

        options = [
            discord.SelectOption(label=f"Изображение {i + 1}", value=str(i), default=(i == current_slide))
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

    async def update_message(self, ctx: discord.Interaction, seleced_slide: int):
        self.select.options[self.current_slide].default = False
        self.select.options[seleced_slide].default = True
        self.current_slide = seleced_slide

        embed = discord.Embed(
            title=f"{self.current_slide + 1}/{len(self.urls)}",
            color=no_color
        )
        embed.set_image(url=self.urls[self.current_slide])
        await ctx.response.edit_message(embed=embed, view=self)

    async def select_callback(self, ctx: discord.Interaction):
        await self.update_message(
            ctx,
            int(self.select.values[0])
        )

    @ui.button(label="<", custom_id="tiktok:left")
    async def prev(self, ctx: discord.Interaction, _):
        await self.update_message(
            ctx,
            (self.current_slide - 1) % len(self.urls)
        )

    @ui.button(label=">", custom_id="tiktok:right")
    async def next(self, ctx: discord.Interaction, _):
        await self.update_message(
            ctx,
            (self.current_slide + 1) % len(self.urls)
        )


