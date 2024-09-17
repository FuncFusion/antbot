from discord.ext import commands
from discord import app_commands

from utils.general import handle_errors
from utils.shortcuts import no_ping
from utils.msg_utils import Emojis

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
	"y": "‖",
	"z": "⨅",
	"а": "ᔑ",
	"б": "ʖ",
	"к": "ᓵ",
	"д": "↸",
	"е": "ᒷ",
	"ф": "⎓",
	"г": "⊣",
	"х": "⍑",
	"и": "╎",
	"ж": "⋮",
	"к": "ꖌ",
	"л": "ꖎ",
	"м": "ᒲ",
	"н": "リ",
	"о": "𝙹",
	"п": "!¡",
	"р": "∷",
	"с": "ᓭ",
	"т": "ℸ",
	"у": "̣",
	"в": "⚍",
	"x": "̇̇/",
	"й": "‖",
	"з": "⨅",
	"ы": "╎",
	"ь": "'",
	"ъ": "'",
	"ё": "‖𝙹",
	"э": "ᒷ",
	"ч": "ᓵ⍑",
	"ш": "ᓭ⍑",
	"щ": "ᓭ⍑ᓵ⍑",
	"я": "‖ᔑ",
	"і": "╎",
	"ї": "‖╎",
	"ю": "‖̣"
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
	"‖": "y",
	"⨅": "z",
	"\u200b": ""
}


class EnchantCommands(commands.Cog):

	@commands.hybrid_command(
		aliases=["ench", "енч", "энч", "зачаровать", "зачарить", "зачарь", "зачаруй", "утср", "утсрфте"],
		description="Переводит текст на язык стола зачарования (Standard Galactic Alphabet).",
		usage="`/enchant <текст>`",
		help="Учтите, что если вы будете пробовать переводить кириллицу, команда сначала переведёт её в латиницу а уже потом на язык стола зачарования.\n### Пример:\n`/enchant калдун это выдуманная абстрактная фигура, состоящая из 10 рублей`")
	@app_commands.describe(text="Текст, который нужно перевести на язык стола зачарований")

	async def enchant(self, ctx, *, text: str):
		enchanted = text.lower()
		for char in normal2sga_table:
			enchanted = enchanted.replace(char, normal2sga_table[char]+"\u200b")
		messages = [enchanted[i:i + 2000] for i in range(0, len(enchanted), 2000)]
		await ctx.reply(messages[0], allowed_mentions=no_ping)
		for message in messages[1:]:
			await ctx.channel.send(message)

	@enchant.error
	async def enchant_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Введите текст, который хотите зачаровать"
			},
		])
		

	@commands.hybrid_command(
		aliases=["unench", "аненч", "анэнч", "раззачаровать", "разчарить", "разчарь", "разчаруй", "гтутср", "гтутсрфте"],
		description="Переводит сообщение с языка стола зачарования",
		usage="`/unenchant <текст>`",
		help="### Пример:\n`/unenchant ꖌ​ᔑ​ꖎ​↸​̣​リ​ ᒷ​ℸ​𝙹​ ⚍​╎​↸​̣​ᒲ​ᔑ​リ​リ​ᔑ​‖ᔑ​ ᔑ​ʖ​ᓭ​ℸ​∷​ᔑ​ꖌ​ℸ​リ​ᔑ​‖ᔑ​ ⎓​╎​⊣​̣​∷​ᔑ​, ᓭ​𝙹​ᓭ​ℸ​𝙹​‖ᔑ​ᓭ⍑ᓵ⍑​ᔑ​‖ᔑ​ ╎​⨅​ 10 ∷​̣​ʖ​ꖎ​ᒷ​‖​`")
	@app_commands.describe(text="Текст, который нужно перевести с языка стола зачарований")

	async def unenchant(self, ctx, *, text: str):
		unenchanted = text
		for char in sga2normal_table:
			unenchanted = unenchanted.replace(char, sga2normal_table[char])
		messages = [unenchanted[i:i + 2000] for i in range(0, len(unenchanted), 2000)]
		await ctx.reply(messages[0], allowed_mentions=no_ping)
		for message in messages[1:]:
			await ctx.channel.send(message)

	@unenchant.error
	async def unenchant_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Введите текст, c которого хотите снять чары"
			}
		])

