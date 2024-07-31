import discord
from discord.ext import commands

from settings import HELP_FORUM_ID

from utils.msg_utils import Emojis
from utils.shortcuts import  no_color


class StartMessage(commands.Cog):
	@commands.Cog.listener("on_thread_create")
	async def new_help_post(self, trd):
		if trd.parent_id == HELP_FORUM_ID:
			# Building embed
			embed = discord.Embed(title=f"{Emojis.pin} Ознакомтесь с правилами получения помощи!", color=no_color, 
				description=f"Если ещё не читали, прочитайте в закреп ветке (https://discord.com/channels/914772142300749854/1021488153909018704) \
				рекомендации к веткам помощи, и о том, как работают некоторые её аспекты. Следование всем рекомендациям \
				(особенно 4 пункту) поможет получить наиболее эффективную помощь. Когда проблема решится, используйте команду </resolve:1250486582109274206>.".replace("\t", ""))
			#
			await trd.send(embed=embed)
			await trd.starter_message.pin()
