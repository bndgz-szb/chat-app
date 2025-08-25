import json
import websockets

from global_variables import CONNECTIONS
from messages import UserListMessage, UserLoginMessage, RegisterAttempt, LoginAttempt

async def sendUserList(websocket):
	msg = UserListMessage(msg_type="user_list", users=list(CONNECTIONS.keys()))
	await websocket.send(json.dumps(msg.__dict__))

def broadcastConnectionsState(messageType, username):
	msg = UserLoginMessage(msg_type=messageType, username=username)
	websockets.broadcast(CONNECTIONS.values(), json.dumps(msg.__dict__))

async def register(attempt: RegisterAttempt):
	# check if username is already in use
	# create user account
	# query user chats
	pass

# returns username on correct login
async def login(attempt: LoginAttempt) -> str:
	# check credentials
	# query user chats
	pass
