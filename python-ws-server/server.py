import json
import asyncio
import websockets

CONNECTIONS = dict()
HISTORY = dict()

async def chat_key(a, b):
	return tuple(sorted([a, b]))

async def sendError(websocket, message):
	await websocket.send(json.dumps({
		"type": "error",
		"message": message
	}))

async def sendMessage(sender, receiver, message):
	# TODO validate message
	jsonMessage = {
		"type": "message",
		"from": sender,
		"to": receiver,
		"message": message
	}
	await CONNECTIONS[receiver].send(json.dumps(jsonMessage))
	HISTORY[chat_key] = jsonMessage

async def sendUserList(websocket):
	jsonMessage = {
		"type": "user_list",
		"users": list(CONNECTIONS.keys())
	}
	await websocket.send(json.dumps(jsonMessage))

def broadcastConnectionsState(messageType, username):
	jsonMessage = {
		"type": messageType,
		"username": username
	}
	websockets.broadcast(CONNECTIONS.values(), json.dumps(jsonMessage))

def broadcastMessage(sender, message):
	jsonMessage = {
		"type": "broadcast",
		"from": sender,
		"message": message
	}

	websockets.broadcast(filter(lambda websocket : websocket != CONNECTIONS[sender], CONNECTIONS.values()), json.dumps(jsonMessage))

# returns username on correct login
async def login(websocket):
	raw = await websocket.recv()
	try:
		data = json.loads(raw)
		assert all(key in data for key in ("type", "username"))
		assert data.get("type") == "login"
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
				assert all(key in data for key in ("type", "from", "to", "message"))
			except (json.JSONDecodeError, AssertionError):
				await sendError(websocket, "Invalid message format")
				continue

			sender = data["from"]
			receiver = data["to"]
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

async def handle(websocket):
	username = await login(websocket)
	if username == "":
		return

	await message_loop(websocket, username)

async def main():
	async with websockets.serve(handle, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

asyncio.run(main())
