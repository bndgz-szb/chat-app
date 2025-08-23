import json
import websockets

from global_variables import CONNECTIONS
from messages import UserListMessage, UserLoginMessage

async def sendUserList(websocket):
	msg = UserListMessage(msg_type="user_list", users=list(CONNECTIONS.keys()))
	await websocket.send(json.dumps(msg.__dict__))

def broadcastConnectionsState(messageType, username):
	msg = UserLoginMessage(msg_type=messageType, username=username)
	websockets.broadcast(CONNECTIONS.values(), json.dumps(msg.__dict__))

# returns username on correct login
async def login(websocket) -> str:
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