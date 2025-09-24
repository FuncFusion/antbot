import discord
from discord import ui, SelectOption as SO
from discord.ext import commands

from asyncio import sleep
from datetime import datetime, timedelta, timezone

from settings import CREATIONS_FORUM_ID, DATAPACKS_TAG, RESOURCEPACKS_TAG, ONLY_CB_TAG, \
	BLOCKBENCH_TAG, VSCODE_TAG, MODS_TAG, PLUGINS_TAG, MISC_TAG, OPTIFINE_TAG, SOLVED_TAG, \
	RESOURCEPACKS_TAGS, DATAPACK_MASTER_ROLE, RESOURCEPACK_MASTER_ROLE
from utils import Emojis, no_color, no_ping, totag, is_moderator, handle_errors, LazyLayout

async def get_author(ctx: discord.Interaction):
	starter_msg = await ctx.channel.fetch_message(ctx.channel.id)
	return await ctx.guild.fetch_member(int(starter_msg.components[0].content.split(">")[0].split("@")[-1]))


class StarterMessage(commands.Cog):

	@commands.Cog.listener("on_thread_create")
	async def new_help_post(self, trd):
		if trd.parent_id == CREATIONS_FORUM_ID:
			layout = LazyLayout(
				ui.TextDisplay(	
					f"## {Emojis.pin} Ознакомьтесь с правилами творчества!\n"
					"Надеемся, что вы уже прочитали правила творчества "
					"(https://discord.com/channels/914772142300749854/1142473873200267314/1142473873200267314). "
					"Если вы хотите поменять картинку на обложке вашего поста, вы **можете это сделать**. Вы можете вставить прямую "
					"ссылку на картинку или ссылку на тот сайт, что уже имеет картинку в своём эмбеде. Также не забывайте, что вы можете "
					"закреплять сообщения в своей ветке, отреагировав с помощью эмодзи :pushpin:."
				)
			)
		for _ in range(10):
			try:
				await trd.send(view=layout)
				await trd.starter_message.pin()
				return
			except discord.errors.Forbidden:
				await sleep(1)
				print("Trying to send starter message again...")


class BetterCallMastersButton(ui.Button):
	def __init__(self):
		super().__init__(
			label="Позвать мастеров", 
			emoji=Emojis.question_mark, 
			custom_id="starter_message:call_masters"
		)
	
	async def callback(self, ctx: discord.Interaction):
		post_author = await get_author(ctx)

		if ctx.user != post_author and not is_moderator(ctx.user):
			raise Exception("No perms")
		if datetime.now().timestamp() - ctx.message.created_at.timestamp() < timedelta(days=1).total_seconds():
			raise Exception("Awaited not enough")
		
		metnions = []
		if DATAPACKS_TAG in ctx.channel.applied_tags:
			metnions.append(f"<@&{DATAPACK_MASTER_ROLE}>")
		if any((tag in ctx.channel.applied_tags for tag in RESOURCEPACKS_TAGS)):
			metnions.append(f"<@&{RESOURCEPACK_MASTER_ROLE}>")
		if not metnions:
			raise Exception("No massters")
		
		await ctx.channel.send(" ".join(metnions))
		await ctx.response.edit_message(view=StarterMessageLayout(call_masters_disabled=True))


class ResolveButton(ui.Button):
	def __init__(self):
		super().__init__(
			label="Проблема решена", 
			emoji=Emojis.check, 
			custom_id="starter_message:resolve"
		)
	
	async def callback(self, ctx: discord.Interaction):
		post_author = await get_author(ctx)
		
		if ctx.user != post_author and not is_moderator(ctx.user):
			raise Exception("No perms")
		
		await ctx.response.send_message(
			view=LazyLayout(ui.TextDisplay(f"# {Emojis.check} Проблема решена!\n"
				"### Любое новое сообщение или реакция снова откроет эту ветку.")
			)
		)
		if len(ctx.channel.applied_tags) == 5:
			await ctx.channel.remove_tags(ctx.channel.applied_tags[-1])
		await ctx.channel.add_tags(SOLVED_TAG)
		await ctx.channel.edit(archived=True)


class StarterMessageLayout(ui.LayoutView):
	def __init__(self, call_masters_disabled = False):
		super().__init__(timeout=None)
		self.cuntainer.call_masters_sec.accessory.disabled = call_masters_disabled

	class Cuntainer(ui.Container):
		text = ui.TextDisplay(f"# {Emojis.pin} Добро пожаловать в помощь\n"
			"Пожалуйста, выберите тэги, которые соответствуют вашей проблеме"
			"в меню ниже"
		)
		selectar = ui.ActionRow()
		sep = ui.Separator()
		call_masters_sec = ui.Section(
			f"Позовите мастеров, если вам не отвечают больше дня",
			accessory = BetterCallMastersButton()
		)
		resolve_sec = ui.Section(
			"Пометьте пост закрытым, когда решите проблему",
			accessory = ResolveButton()
		)

		@selectar.select(
			custom_id="tickets:tags_select",
			placeholder="Выбирете тэги со списка", 
			min_values=1, 
			max_values=4, 
			options=[
				SO(label="Датапаки", emoji=Emojis.deta_rack, value=str(DATAPACKS_TAG.id)),
				SO(label="Ресурспаки", emoji=Emojis.resource_rack, value=str(RESOURCEPACKS_TAG.id)),
				SO(label="Только КБ", emoji=Emojis.mcf_load, value=str(ONLY_CB_TAG.id)),
				SO(label="Другое", emoji=Emojis.misc, value=str(MISC_TAG.id)),
				SO(label="Blockbench", emoji=Emojis.models, value=str(BLOCKBENCH_TAG.id)),
				SO(label="VS Code", emoji=Emojis.vsc, value=str(VSCODE_TAG.id)),
				SO(label="Плагины", emoji=Emojis.archive, value=str(PLUGINS_TAG.id)),
				SO(label="Моды", emoji=Emojis.jar, value=str(MODS_TAG.id)),
				SO(label="Оптифайн", emoji=Emojis.cross, value=str(OPTIFINE_TAG.id)),
			]
		)
		async def tags_selection(self, ctx: discord.Interaction, _):
			post_author = await get_author(ctx)
			if ctx.user != post_author and not is_moderator(ctx.user):
				raise Exception("No perms")
			
			tags_to_apply = tuple(totag(int(i)) for i in ctx.data["values"])
			tags_to_remove = tuple(tag for tag in ctx.channel.applied_tags if tag != SOLVED_TAG)

			await ctx.channel.remove_tags(*tags_to_remove)
			await ctx.channel.add_tags(*tags_to_apply)
			await ctx.response.send_message(f"{Emojis.check} Тэги успешно отредактикрованы", ephemeral=True)

	cuntainer = Cuntainer()

	async def on_error(self, ctx: discord.Interaction, error, _):
		await handle_errors(ctx, error, [
			{
				"contains": "No perms",
				"msg": "Вы не являетесь ни автором ветки, ни модератором"
			},
			{
				"contains": "Awaited not enough",
				"msg": "Подождите хотя бы 24 часа, перед тем как звать мастеров на помощь"
			},
			{
				"contains": "No massters",
				"msg": "Не обнаружено дп/рп тэгов в этом посте"
			}
		])

