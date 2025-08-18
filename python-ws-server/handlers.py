import json
import websockets

from global_variables import CONNECTIONS
from global_variables import HISTORY
from messages import *

async def chat_key(a, b):
	return tuple(sorted([a, b]))

async def sendError(websocket, message):
	msg = ErrorMessage(msg_type="error", message=message)
	await websocket.send(json.dumps(msg.__dict__))

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

async def sendUserList(websocket):
	msg = UserListMessage(msg_type="user_list", users=list(CONNECTIONS.keys()))
	await websocket.send(json.dumps(msg.__dict__))

def broadcastConnectionsState(messageType, username):
	msg = UserLoginMessage(msg_type="user_login", username=username)
	websockets.broadcast(CONNECTIONS.values(), json.dumps(msg.__dict__))

def broadcastMessage(sender, message):
	msg = BroadcastMessage(msg_type="broadcast", sender=sender, message=message)
	websockets.broadcast(filter(lambda websocket : websocket != CONNECTIONS[sender], CONNECTIONS.values()), json.dumps(msg.__dict__))

# returns username on correct login
async def login(websocket):
	raw = await websocket.recv()
	try:
		data = json.loads(raw)
		assert all(key in data for key in ("msg_type", "username"))
		assert data.get("msg_type") == "login"
	except (json.JSONDecodeError, AssertionError):
		await websocket.close(code=4000, reason="Login required")
		return ""

	# TODO ban empty username
	username = data["username"]
	if username in CONNECTIONS.keys():
		await websocket.close(code=4001, reason="Username already taken")
		return ""
	
	await sendUserList(websocket)
	broadcastConnectionsState("user_login", username)

	CONNECTIONS[username] = websocket
	print(f"[LOGIN] {username} connected")
	return username

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

			sender = data["sender"]
			receiver = data["target"]
			message = data["message"]

			if receiver == "":
				broadcastMessage(sender, message)
				continue

			if websocket != CONNECTIONS[sender]: # check sender address
				await websocket.close(code=4002, reason="Can't send messages in someone else's name")

			elif receiver not in CONNECTIONS.keys(): # check if receiver is online
				await sendError(websocket, "User currently offline")

			else: # send message to receiver, save to history
				try:
					await sendMessage(sender, receiver, message)
				except:
					await sendError(websocket, "User disconnected before receiving the message")
	except:
		print(f"[CLOSE] {username} closed connection")
	finally:
		print(f"[DISCONNECTED] {username} removed from active list")
		del CONNECTIONS[username]
		broadcastConnectionsState("user_logout", username)