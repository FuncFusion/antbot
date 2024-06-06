import re

from cogs.mc.highlighter.main import Hl as hl

from utils.fake_user import fake_send
from utils.tree_gen import generate_tree
from utils.msg_utils import split_msg

async def formatter_listener(msg):
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
