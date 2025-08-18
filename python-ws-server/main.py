import asyncio
import signal

from server import main
from global_variables import SHUTDOWN

def shutdown():
  print("Setting shutdown event")
  SHUTDOWN.set()

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
