import asyncio
import signal
import websockets

from handlers import handle_auth
from global_variables import CONNECTIONS, SHUTDOWN

def shutdown():
  print("Setting shutdown event")
  SHUTDOWN.set()

async def main():
	async with websockets.serve(handle_auth, "0.0.0.0", 8765) as server:
		print("WebSocket server started.")
		await SHUTDOWN.wait()
		print("Shutdown signal received, closing connections...")
		for user, ws in CONNECTIONS.items():
			await ws.close(code=1001, reason="Server shutdown")
		CONNECTIONS.clear()

# Register signal handlers
loop = asyncio.get_event_loop()
for sig in (signal.SIGINT, signal.SIGTERM):
  loop.add_signal_handler(sig, shutdown)

# Start the main loop
try:
  loop.run_until_complete(main())
finally:
  loop.close()
  print("Event loop closed.")
