import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING

from re import search, MULTILINE
from typing import List

from utils.general import handle_errors
from utils.msg_utils import Emojis
from utils.shortcuts import no_color, no_ping
from utils.validator import validate, all_valid


with open("wiki/commands.md", "r", encoding="utf-8") as c:
	with open("wiki/features.md", "r", encoding="utf-8") as f:
		wiki = f"{c.read()}\n{f.read()}"


class HelpCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.hybrid_command(aliases=["h", "?", "х", "хелп", "помощь", "рудз"], 
		description="Показывает как пользоватся командами/фичами антбота")
	async def help(self, ctx, *, feature):
		feature = validate(feature, features, 3.5)
		commands = await self.bot.tree.fetch_commands()
		mention = feature
		for command in commands:
			if feature == command.name:
				mention = command.mention
				break
		if not feature:
			raise AttributeError("wrong command/feature")
		guide = search(fr"(^## {feature}[\S\s]+?)(> ?\n> !\[[\w ]*\]\(([\w-]+\.png)|\n\n)", wiki, MULTILINE)
		if guide.group(2).endswith(".png"):
			file = discord.File(f"wiki/{guide.group(3)}", filename="image.png")
		else:
			file = MISSING
		await ctx.reply(guide.group(1).replace(f"## {feature}", f"## {mention}"), file=file, allowed_mentions=no_ping)
	
	@help.autocomplete("feature")
	async def help_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
		global offered_features
		if curr != "":
			offered_features = [app_commands.Choice(name=feature, value=feature) for feature in all_valid(curr, features)][:25]
		return offered_features

	@help.error
	async def help_error(self, ctx, error):
		await handle_errors(ctx, error, [
			{
				"exception": commands.MissingRequiredArgument,
				"msg": "Не хватает аргументов"
			},
			{
				"contains": "AttributeError",
				"msg": "Не существует такой команды/фичи"
			}
		])

features = {
	"Оповещения о приветствии и прощании": ["привет пока","привет","пока"],
	"Форматтер": ["форматтер", "форматтер сообщений", "хайлайтер", "генератор древа файлов", "formatter", "highlighter", 
		"tree generator"],
	"Закреп в своих ветках помощи/творчества": ["пин", "закреп", "pin"],
	"Система собственных голосовых каналов": ["система гк", "кастом гк", "гк", "свои гк", "голосовые каналы"],
	"FAQшки": ["?", "faq", "FAQS", "факушки", "факу"],
	"Уведомление о выходе новой версии майна": ["новые снапшоты","снапшот скрейпер","snapshot scraper","new snapshots","снапшоты"],
	"Логи": ["logs","дщпы"],
	"status": ["ыефегы", "статус"],
	"edit": ["изменить", "эдит", "увше"],
	"ping": ["p", "latency", "пинг", "п", "з", "зштп", "дфеутсн"],
	"say": ["s", "сказать", "молвить", "сей", "сэй", "ыфн", "ы"],
	"enchant": ["ench", "енч", "энч", "зачаровать", "зачарить", "зачарь", "зачаруй", "утср", "утсрфте"],
	"unenchant": ["unench", "аненч", "анэнч", "раззачаровать", "разчарить", "разчарь", "разчаруй", "гтутср", "гтутсрфте"],
	"look-for": [],
	"random": ["rand", "r", "rng", "рандом", "ранд", "случайный-ответ", "сгенерь-ответ", "кфтвщь", "кфтв", "к", "ктп"],
	"randomrange": ["random-range", "rr", "рандом-число", "сгенерь-число", "кфтвщь-кфтпу", "кк"],
	"giveaway": ["ga", "розыгрыш"],
	"blacklist": ["bl", "бл", "чс"],
	"whitelist": ["wl", "вл", "бс"],
	"transfer-ownership": ["передать-права", "to", "пп"],
	"idea": ["швуф", "идея", "suggest", "предложить", "ыгппуые"],
	"approve-idea": [],
	"disapprove-idea": [],
	"server-info": ["serverinfo", "info", "server", "si", "сервер-инфо", "инфо", "сервер", "си", "ыукмукштащ", "штащ", "ыукмук", "ыш"],
	"view-voters": [],
	"help": ["h", "?", "х", "хелп", "помощь", "рудз"],
	"link": ["l", "л", "линк", "ссылка", "дштл", "ccskrf"],
	"resolve": ["solve", "ыщдму", "куыщдму", "решено", "ресолв", "солв"],
	"syntax": ["stx", "ынтефч", "ыея", "синтакс", "синтаксис", "сткс"],
	"packformat": ["mcmetaformat", "pack-format", "pack_format", "packmcmetaformat", "pf", "пакформат", "пак-формат", "пак_формат", "мсметаформат", "пакмсметаформат", "пф", "зфслащкьфе", "за"],
	"template": ["tl", "темплейт", "тэмплейт", "еуьздфеу", "шаблон"],
	"clear": ["сдуфк", "клир", "очистить"],
	"ban": ["ифт", "бан", "банчек", "заблокировать"],
	"unban": ["гтифт", "анбан", "разблокировать"],
	"kick": ["лшсл", "кик", "изгнать"],
	"mute": ["ьгеу", "мут"]
}
offered_features = [app_commands.Choice(name=feature, value=feature) for feature in list(features)][:25]
