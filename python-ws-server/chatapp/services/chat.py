import json

from global_variables import CONNECTIONS, HISTORY
from messages import UnicastMessage

async def chat_key(a, b):
	return tuple(sorted([a, b]))

async def sendMessage(sender, target, message):
	# TODO validate message content
	msg = UnicastMessage(
		msg_type="message",
		sender=sender,
		target=target,
		message=message
	)
	await CONNECTIONS[target].send(json.dumps(msg.__dict__))
	HISTORY[chat_key] = msg.__dict__