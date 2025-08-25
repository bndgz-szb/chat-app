import json
import websockets

from dataclasses import fields
from global_variables import CONNECTIONS
from messages import *
from services.auth import broadcastConnectionsState
from typing import TypedDict, List

class SuccessResponse(TypedDict):
	status: str
	username: str
	chats: List[int]

class ErrorResponse(TypedDict):
	status: str
	error: str

Response = SuccessResponse | ErrorResponse

async def handle(websocket):
	raw = await websocket.recv()
	username = await handle_auth(raw)
	# TODO handle error
	# websocket.send(chat_list)

	await message_loop(websocket, username)

async def handle_auth(raw_json) -> Response:
	try:
		data = json.loads(raw_json)
		if data.get("msg_type") == "login":
			assert all(key in data for key in fields(LoginAttempt))
		elif data.get("msg_type") == "register":
			assert all(key in data for key in fields(RegisterAttempt))
		else:
			raise AssertionError()
	except json.JSONDecodeError:
		return {
			"status": "error",
			"error": "JSON decode error"
		}
	except AssertionError:
		return {
			"status": "error",
			"error": "Wrong message format"
		}
	
	if data.get("msg_type") == "login":
		response = await services.auth.login(LoginAttempt(**data))
	elif data.get("msg_type") == "register":
		response = await services.auth.register(RegisterAttempt(**data))
	# TODO check response
	return {
		"status": "ok",
		"username": response.username,
		"chats": response.chats
	}

async def sendError(websocket, message):
	msg = ErrorMessage(msg_type="error", message=message)
	await websocket.send(json.dumps(msg.__dict__))

def broadcastMessage(sender, message):
	msg = BroadcastMessage(msg_type="broadcast", sender=sender, message=message)
	websockets.broadcast(filter(lambda websocket : websocket != CONNECTIONS[sender], CONNECTIONS.values()), json.dumps(msg.__dict__))

async def message_loop(websocket, username):
	try:
		async for message in websocket:
			# check message format
			try:
				data = json.loads(message)
				assert all(key in data for key in ("msg_type", "sender", "target", "message"))
			except (json.JSONDecodeError, AssertionError):
				await sendError(websocket, "Invalid message format")
				continue

			parsed = UnicastMessage(**data)

			if parsed.target == "":
				broadcastMessage(parsed.sender, parsed.message)
				continue

			if websocket != CONNECTIONS[parsed.sender]: # check sender address
				await websocket.close(code=4002, reason="Can't send messages in someone else's name")

			elif parsed.target not in CONNECTIONS.keys(): # check if receiver is online
				await sendError(websocket, "User currently offline")

			else: # send message to receiver, save to history
				try:
					await sendMessage(parsed.sender, parsed.target, parsed.message)
				except:
					await sendError(websocket, "User disconnected before receiving the message")
	except:
		print(f"[CLOSE] {username} closed connection")
	finally:
		print(f"[DISCONNECTED] {username} removed from active list")
		del CONNECTIONS[username]
		broadcastConnectionsState("user_logout", username)