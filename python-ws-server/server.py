import json
import asyncio
import websockets

CONNECTIONS = dict()

async def login(websocket):
	raw = await websocket.recv()
	try:
		data = json.loads(raw)
	except:
		await websocket.close(code=4000, reason="Login required")
		return ""

	if data.get("type") != "login" or not data.get("username"):
		await websocket.close(code=4000, reason="Login required")
		return ""

	username = data["username"]
	if username in CONNECTIONS:
		await websocket.close(code=4001, reason="Username already taken")
		return ""
	
	CONNECTIONS[username] = websocket
	print(f"[LOGIN] {username} connected")
	return username

async def message_loop(websocket, username):
	try:
		async for message in websocket:
			websockets.broadcast(CONNECTIONS.values(), message)
	
	finally:
		print(f"[DISCONNECTED] {username} removed from active list")
		del CONNECTIONS[username]

async def handle(websocket):
	username = await login(websocket)
	if username == "":
		return

	await message_loop(websocket, username)

async def main():
	async with websockets.serve(handle, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

asyncio.run(main())
