import discord
from discord.ext import commands
from discord import app_commands


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

class FunCommands(commands.Cog):
	def __init__(self, bot):
		
		@bot.hybrid_command(aliases=["ench", "зачаровать", "зачарить", "зачарь", "зачаруй"],
					  description="Переводит сообщение на язык стола зачарования")
		async def enchant(ctx, *, text: str):
			enchanted = text
			for char in normal2sga_table:
				enchanted = enchanted.replace(char, normal2sga_table[char]+"\u200b")
			await ctx.send(enchanted)
		
		@bot.hybrid_command(aliases=["unench", "раззачаровать", "разчарить", "разчарь", "разчаруй"],
					  description="Переводит сообщение с языка стола зачарования")
		async def unenchant(ctx, *, text: str):
			unenchanted = text
			for char in sga2normal_table:
				unenchanted = unenchanted.replace(char, sga2normal_table[char])
			await ctx.send(unenchanted)
