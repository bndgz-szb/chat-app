import asyncio
import websockets

CONNECTIONS = set()

async def handle(websocket):
	# Add to connections
	if websocket not in CONNECTIONS:
		print(f"[CONNECTED]: {websocket.remote_address}")
		CONNECTIONS.add(websocket)

	try:
		async for message in websocket:
			websockets.broadcast(CONNECTIONS, message)
	
	finally:
		print(f"[DISCONNECTED] {websocket.remote_address} removed from active list")
		CONNECTIONS.remove(websocket)

async def main():
	async with websockets.serve(handle, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

asyncio.run(main())
