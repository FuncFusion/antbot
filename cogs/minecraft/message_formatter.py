from discord.ext import commands

import re

from utils.highlighter.main import Hl as hl

from utils.fake_user import fake_send
from utils.tree_gen import generate_tree
from utils.msg_utils import split_msg


class MessageFormatter(commands.Cog):
	@commands.Cog.listener("on_message")
	async def formatter(self, msg):
		if "```mcf" in msg.content or "```tree" in msg.content:
			formatted = msg.content
			code_blocks = re.findall(r"(```(tree|mcf)\n([^`]+)```)", msg.content)
			for block in code_blocks:
				if block[1] == "tree":
					formatted = formatted.replace(block[0], generate_tree(block[2]))
				else:
					formatted = formatted.replace(block[0], f"```ansi\n{hl.highlight(block[2])}\n```")
			await msg.delete()
			await fake_send(msg.author, msg.channel, split_msg(formatted), msg.attachments)
