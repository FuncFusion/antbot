import discord
from discord.ext import commands
from discord import app_commands
from random import randint, choice
import re

from Levenshtein import distance

from settings import LOOK_FOR_ID
from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_ping, no_color

normal2sga_table = {
	"a": "ᔑ",
	"b": "ʖ",
	"c": "ᓵ",
	"d": "↸",
	"e": "ᒷ",
	"f": "⎓",
	"g": "⊣",
	"h": "⍑",
	"i": "╎",
	"j": "⋮",
	"k": "ꖌ",
	"l": "ꖎ",
	"m": "ᒲ",
	"n": "リ",
	"o": "𝙹",
	"p": "!¡",
	"q": "ᑑ",
	"r": "∷",
	"s": "ᓭ",
	"t": "ℸ",
	"u": "̣",
	"v": "⚍",
	"w": "∴",
	"x": "̇̇/",
	"y": "||",
	"z": "⨅"
}
sga2normal_table = {
	"ᔑ": "a",
	"ʖ": "b",
	"ᓵ": "c",
	"↸": "d",
	"ᒷ": "e",
	"⎓": "f",
	"⊣": "g",
	"⍑": "h",
	"╎": "i",
	"⋮": "j",
	"ꖌ": "k",
	"ꖎ": "l",
	"ᒲ": "m",
	"リ": "n",
	"𝙹": "o",
	"!¡": "p",
	"ᑑ": "q",
	"∷": "r",
	"ᓭ": "s",
	"ℸ": "t",
	"̣": "u",
	"⚍": "v",
	"∴": "w",
	"̇̇/": "x",
	"||": "y",
	"⨅": "z",
	"\u200b": ""
}

class FunCommands(commands.Cog, name="Развлечения"):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.hybrid_command(aliases=["ench", "зачаровать", "зачарить", "зачарь", "зачаруй", "утср", "утсрфте"],
		description="Переводит сообщение на язык стола зачарования")
	@app_commands.describe(text="Текст, который нужно перевести на язык стола зачарований")
	async def enchant(self, ctx, *, text: str):
		enchanted = text
		for char in normal2sga_table:
			enchanted = enchanted.replace(char, normal2sga_table[char]+"\u200b")
		await ctx.reply(enchanted, allowed_mentions=no_ping)
	@enchant.error
	async def enchant_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Введите текст который хотите зачаровать"
			}
		])
		
	@commands.hybrid_command(aliases=["unench", "раззачаровать", "разчарить", "разчарь", "разчаруй", "гтутср", "гтутсрфте"],
		description="Переводит сообщение с языка стола зачарования")
	@app_commands.describe(text="Текст, который нужно перевести с языка стола зачарований")
	async def unenchant(self, ctx, *, text: str):
		unenchanted = text
		for char in sga2normal_table:
			unenchanted = unenchanted.replace(char, sga2normal_table[char])
		await ctx.reply(unenchanted, allowed_mentions=no_ping)
	@unenchant.error
	async def unenchant_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": f"{Emojis.exclamation_mark} Введите текст который хотите раззачаровать"
			}
		])

	@commands.hybrid_command(aliases=["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
		description="Генерирует рандомное число в заданном промежутке")
	@app_commands.describe(minimum="Минимальное число в промежутке", maximum="Максимальное число в промежутке")
	async def randomrange(self, ctx, minimum: str='-2147483648', maximum: str='2147483647'):
		minInt, maxInt = -2147483648, 2147483647
		clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
		minimum, maximum = clamp(int(float(minimum)), minInt, maxInt), clamp(int(float(maximum)), minInt, maxInt)
		minimum = min(minimum, maximum)
		maximum = max(minimum, maximum)
		result = randint(minimum, maximum)
		embed = discord.Embed(color=no_color, title=f"Рандомное число между {minimum} и {maximum}:")
		embed.add_field(name=result, value='', inline=True)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@randomrange.error
	async def randomrange_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "ValueError",
				"msg": f"{Emojis.exclamation_mark} Допускаются только целочисленные занчения"
			}
		])

	@commands.hybrid_command(aliases=["rand", "r", "rng", "рандом", "ранд", "случайный-ответ", "сгенерь-ответ", "кфтвщь", "кфтв", "к", "ктп"],
		description="Выдаёт случайный ответ из заданных на вопрос. [text] разделяется символом \"|\" или переносом строки")
	@app_commands.describe(text="Текст вопроса и ответов. Разделяются символом \"|\" или переносом строки")
	async def random(self, ctx, *, text: str):
		pattern = r'[|\n]'
		args = re.split(pattern, text)[1:]
		title = re.split(pattern, text)[0]
		result = choice(args)
		embed = discord.Embed(title=title, color=no_color)
		embed.add_field(name="Ответ:", value=result, inline=False)
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	@random.error
	async def random_error(self, ctx, error):
		embed = discord.Embed(title=f"{Emojis.exclamation_mark} Не хватает аргументов?", color=no_color)
		embed.add_field(name="Ответ:", value="Да")
		await ctx.reply(embed=embed, allowed_mentions=no_ping)
	
	@commands.hybrid_command(name="look-for", aliases=["lf", "дщщл-ащк", "да", "ищу-тиммейта"],
		description="Создаёт пост в 🔍・поиск-тимы о поиске тиммейта")
	@app_commands.describe(game="Игра", details="Описание (айпи сервера/приглашение и тд)")
	async def look_for(self, ctx, game: str, *, details: str):
		games = {
			"minecraft": {
				"banners_count": 3,
				"ru_name": "майнкрафт",
				"accusative": "майнкрафта"
			},
			"terraria": {
				"banners_count": 0,
				"ru_name": "террария",
				"accusative": "террарии"
			},
			"gartic": {
				"banners_count": 0,
				"ru_name": "гартик",
				"accusative": "гартика"
			},
			"other": {
				"banners_count": 0,
				"ru_name": game,
				"accusative": game
			}
		}
		for game_name in games:
			if distance(game, game_name) <= len(game_name)/2 \
				or distance(game, games[game_name]["ru_name"]) <= len(games[game_name]["ru_name"])/2:
				game = game_name
				break
		else:
			game = "other"
		look_for_channel = await self.bot.fetch_channel(LOOK_FOR_ID)
		embed = discord.Embed(title=f"{Emojis.spyglass} Ищу тиммейта для {games[game]["accusative"]}", color=no_color)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
		embed.add_field(name="Подробности", value=details, inline=False)
		embed.add_field(name=f"{Emojis.check} Присоединились", value="")
		embed.add_field(name=f"{Emojis.cross} Отклонили", value="")
		embed.set_footer(text=str(ctx.author.id))
		if game in games:
			game_banner = discord.File(f"assets/game_banners/{game}{randint(0, games[game]["banners_count"])}.png", filename="say_gex.png")
			embed.set_image(url="attachment://say_gex.png")
		lf_msg = await look_for_channel.send(embed=embed, view=LookFor(), file=game_banner)
		await lf_msg.create_thread(name="Обсуждение", reason="Auto-thread for look for teammate")
		await ctx.reply(f"{Emojis.check} Пост создан: {lf_msg.jump_url}", allowed_mentions=no_ping)
	@look_for.error
	async def lf_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"contains": "game",
				"msg": f"{Emojis.exclamation_mark} Укажите игру, для которой ищите тиммейта"
			},
			{
				"contains": "details",
				"msg": f"{Emojis.exclamation_mark} Укажите подробности (айпи сервера/ссылка с приглашением и тд)"
			}
		])


class Giveaway(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Принять участие", emoji=Emojis.check, custom_id="giveaway:take-part")
	async def take_part(self, ctx, button):
		pass


class LookFor(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	async def response(ctx, action):
		embed = ctx.message.embeds[0]
		joined_users = embed.fields[1].value.split("\n")
		declined_users = embed.fields[2].value.split("\n")
		action_users_list = joined_users if action == "join" else declined_users
		opposite_users_list = declined_users if action == "join" else joined_users
		usr_ping = ctx.user.mention
		if usr_ping not in action_users_list:
			action_users_list.append(usr_ping)
		else:
			action_users_list.remove(usr_ping)
		if usr_ping in opposite_users_list:
			opposite_users_list.remove(usr_ping)
		embed.set_field_at(1, name=embed.fields[1].name, value="\n".join(joined_users))
		embed.set_field_at(2, name=embed.fields[2].name, value="\n".join(declined_users))
		await ctx.response.edit_message(embed=embed, attachments=[])
	
	@discord.ui.button(label="Присоединится", emoji=Emojis.check, custom_id="look-for:join")
	async def join(self, ctx, button):
		await LookFor.response(ctx, "join")
	
	@discord.ui.button(label="Отказатся", emoji=Emojis.cross, custom_id="look-for:decline")
	async def decline(self, ctx: discord.Interaction, button: discord.ui.Button):
		await LookFor.response(ctx, "decline")
	
	@discord.ui.button(label="Пингануть участников", emoji=Emojis.users, custom_id="look-for:ping-all")
	async def ping_all(self, ctx: discord.Interaction, button: discord.ui.Button):
		joined_users = ctx.message.embeds[0].fields[1].value.split("\n")
		if str(ctx.user.id) == ctx.message.embeds[0].footer.text:
			if joined_users[0] not in ["", ctx.user.mention]:
				await ctx.response.send_message(" ".join(joined_users) + f" вас зовёт {ctx.user.mention}")
			else:
				await ctx.response.send_message(f"{Emojis.exclamation_mark} Пока нет кого пинговать", ephemeral=True)
		else:
			await ctx.response.send_message(f"{Emojis.exclamation_mark} Вы не являеетесь автором поста", ephemeral=True)
	
