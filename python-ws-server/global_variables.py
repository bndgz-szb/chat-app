import asyncio

CONNECTIONS = dict()
HISTORY = dict()
SHUTDOWN = asyncio.Event()
