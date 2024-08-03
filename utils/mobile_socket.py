import asyncio
import aiohttp
from discord.gateway import DiscordWebSocket

async def mobile(self, status=None) -> None:
	"""Sends the IDENTIFY packet."""
	payload = {
		'op': self.IDENTIFY,
		'd': {
			'token': self.token,
			'properties': {
				'os': 'SayGexOS',
				'browser': f'Discord Android',
				'device': 'FF FG 1 "AntBot"',
			},
			'compress': True,
			'large_threshold': 250,
		},
	}

	if self.shard_id is not None and self.shard_count is not None:
		payload['d']['shard'] = [self.shard_id, self.shard_count]

	state = self._connection
	if state._activity is not None or state._status is not None:
		payload['d']['presence'] = {
			'status': state._status if not status else status,
			'game': state._activity,
			'since': 0,
			'afk': False,
		}

	if state._intents is not None:
		payload['d']['intents'] = state._intents.value

	await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
	await self.send_as_json(payload)

DiscordWebSocket.identify = mobile