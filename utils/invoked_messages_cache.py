from asyncio import sleep, Lock, create_task
from json import load, dump


cache_path = "utils/invoked_messages_cache.json"
cache_lock = Lock()
with open(cache_path, "w")as f:
	f.write("{}")


def check_author_from_cache(author_id, message_id):
	try:
		with open(cache_path, "r")as f:
			cache = load(f)
			return message_id in cache.get(str(author_id), [])
	except: return False


async def cache_message_author(author_id: int, message_ids: list[int]):
	async with cache_lock:
		with open(cache_path, "r")as f:
			cache = load(f)

		key = str(author_id)
		if key not in cache:
			cache[key] = []
		cache[key].extend(message_ids)
		
		with open(cache_path, "w")as f:
			dump(cache, f)
	create_task(schedule_clear_cache(author_id=author_id, message_ids=message_ids))
	

async def schedule_clear_cache(author_id: int, message_ids: int):
	await sleep(360)

	async with cache_lock:
		with open(cache_path, "r")as f:
			cache = load(f)
		
		key = str(author_id)
		for id in message_ids:
			cache[author_id].remove(id)
		if not cache[key]:
			del cache[key]
		
		with open(cache_path, "w")as f:
			dump(cache, f)
