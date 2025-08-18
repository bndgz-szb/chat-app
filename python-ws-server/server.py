import websockets

from handlers import login
from handlers import message_loop
from global_variables import CONNECTIONS
from global_variables import SHUTDOWN

async def handle(websocket):
	username = await login(websocket)
	if username == "":
		return

	await message_loop(websocket, username)

async def main():
	async with websockets.serve(handle, "0.0.0.0", 8765) as server:
		print("WebSocket server started.")
		await SHUTDOWN.wait()
		print("Shutdown signal received, closing connections...")
		for user, ws in CONNECTIONS.items():
			await ws.close(code=1001, reason="Server shutdown")
		CONNECTIONS.clear()