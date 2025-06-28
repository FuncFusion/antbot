import discord
from discord.ext import commands

import subprocess
import tempfile
import os
import asyncio
import aiohttp
from PIL import Image
from io import BytesIO

from utils import handle_errors, no_color, no_ping, edit_image, Emojis

image_types = (
	"bmp", "dds", "gif", "ico", "im",
	"jpg", "jpeg", "msp", "pcx", "png",
	"pbm", "pgm", "ppm", "pnm", "psd",
	"tif", "tiff", "webp", "xbm", "xpm"
)
video_types = (
	"mp4", "wmv", "mkv", "webm", "mov",
	"avi", "flv", "f4v", "swf", "mts", "mpeg", "mpg",
	"vob", "rm", "rmvb", "ogv", "asf", "3gp", "divx",
	"xvid", "ts", "dvr-ms", "m4v"
)
supported_types = image_types + video_types
url = "https://catbox.moe/user/api.php"

mid_quality_filter = [
	"-vf", "fps=30,scale='iw*2/3':-1:flags=lanczos",
	"-q:v", "50",
]
low_quality_filter = [
	"-vf", "fps=25,scale='iw/3':-1:flags=lanczos",
	"-q:v", "40",
]


class GifCommand(commands.Cog):
	@commands.hybrid_command(
		aliases=["пша", "гиф", "гниф", "uba"],
		description="Конвертирует изображение/видео в гнифку",
		usage="`/gif <медиа файл>`",
		help="")

	async def gif(
		self, 
		ctx: commands.Context, 
		media: discord.Attachment
	):
		media_bytes = await media.read()
		media_extension = media.filename.split(".")[-1]

		if media_extension == "gif":
			raise Exception("Already gif")
		if len(media_bytes)/1000000 > 50 and not ctx.author.guild_permissions.administrator:
			raise Exception("Too large")
		
		gifed_name = media.filename.replace(media_extension, "gif")

		if media_extension in image_types:
			gifed = edit_image(
				Image.open(BytesIO(media_bytes)),
				"gif",
				lambda image: image.convert(mode="RGBA")
			)
			discorded_gifed = discord.File(gifed, filename=gifed_name)
			await ctx.reply(file=discorded_gifed, allowed_mentions=no_ping)

		elif media_extension in video_types:
			loading_gif = discord.File("assets/loading_gif.gif")
			loading_msg = await ctx.reply("Конвертирую в гифку...", file=loading_gif, allowed_mentions=no_ping)
			gif_link = await video2webp(media_bytes, loading_msg)
			await loading_msg.edit(content=gif_link, attachments=[], allowed_mentions=no_ping)
		
		else:
			raise Exception("Unsupported format")


	@gif.error
	async def gif_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "Already gif",
				"msg": "https://tenor.com/view/side-eye-rock-the-rock-gif-6658795805713564985" 
			},
			{
				"contains": "Upload fail",
				"msg": "Загрузка не удалась"
			},
			{
				"contains": "Unsupported format",
				"msg": "Этот формат не поддерживается"
			},
			{
				"contains": "ffmpeg",
				"msg": "Ошибка конвертации"
			},
			{
				"contains": "Too large",
				"msg": "Слишком большой файл"
			},
			{
				"contains": "UnidentifiedImageError",
				"msg": "Изображение повреждено"
			}
		])
	

async def video2webp(file: bytes, msg: discord.Message):
	input_temp = None
	output_temp = None
	
	try:
		input_temp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
		output_temp = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
		
		input_path = input_temp.name
		output_path = output_temp.name
		
		input_temp.write(file)
		input_temp.close() 
		output_temp.close()
		
		cmd = [
			"ffmpeg",
			"-y",
			"-i", input_path,
			"-probesize", "100M",
			"-analyzeduration", "200M",
			"-preset", "default",
			"-lossless", "0",
			"-loop", "0",
			"-an",
		]

		size_mb = len(file) / 1000000

		if size_mb > 480:
			raise Exception("Too large")
		elif size_mb > 180:
			cmd.extend(low_quality_filter)
		elif size_mb > 80:
			cmd.extend(mid_quality_filter)
		cmd.extend(["-f", "webp", output_path])
		
		process = await asyncio.create_subprocess_exec(
			*cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		
		stdout, stderr = await process.communicate()
		
		if process.returncode != 0:
			error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Unknown FFmpeg error"
			raise Exception(f"FFmpeg failed: {error_msg}")
		
		if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
			raise Exception("FFmpeg produced no output")
		
		with open(output_path, 'rb') as f:
			webp_data = f.read()
		
		if not webp_data:
			raise Exception("Empty output file")
		
		await msg.edit(content="Загружаю на catbox...", allowed_mentions=no_ping)
		
		async with aiohttp.ClientSession() as session:
			form = aiohttp.FormData()
			form.add_field('reqtype', 'fileupload')
			form.add_field('fileToUpload', webp_data, filename="converted.webp", content_type='image/webp')

			async with session.post(url, data=form) as resp:
				if resp.status == 200:
					result = await resp.text()
					if result.startswith('http'):
						return result
					else:
						raise Exception(f"Upload failed: {result}")
				else:
					raise Exception(f"Upload failed with status {resp.status}")
	
	except Exception as e:
		await msg.delete()
		if "Too large" in str(e) or "ffmpeg" in str(e):
			raise e
		else:
			raise Exception(f"Conversion error: {str(e)}")
	
	finally:
		for temp_file in [input_temp, output_temp]:
			if temp_file and temp_file.name:
				try:
					if not temp_file.closed:
						temp_file.close()
					if os.path.exists(temp_file.name):
						os.unlink(temp_file.name)
				except Exception as cleanup_error:
					print(f"Warning: Could not clean up temp file {temp_file.name}: {cleanup_error}")


class GifizeView(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Конвертировать в гиф", custom_id="gifize:togif")
	async def togif(self, ctx: discord.Interaction, _):
		if (
			ctx.message.interaction and ctx.message.interaction.user == ctx.user
			or
			not ctx.message.reference.fail_if_not_exists and
			(ref:=await ctx.channel.fetch_message(ctx.message.reference.jump_url.split("/")[-1])) and 
			ref.author == ctx.user
		):
			await ctx.response.defer()
			attachment = ctx.message.attachments[0]
			image = Image.open(BytesIO(await attachment.read()))
			gifed = edit_image(
				image,
				"gif",
				lambda im: im.convert(mode="RGBA")
			)
			discorded_gifed = discord.File(
				gifed, 
				".".join(attachment.filename.split(".")[:-1]) + ".gif"
			)
			await ctx.message.edit(attachments=[discorded_gifed], view=None)
		else:
			await ctx.response.send_message(
				f"{Emojis.exclamation_mark} Вы не являетесь автором команды",
				ephemeral=True
			)

