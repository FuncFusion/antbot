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


class EnchantCommands(commands.Cog):

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
				"msg": f"{Emojis.exclamation_mark} Введите текст c которого хотите снять чары"
			}
		])
