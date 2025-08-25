import json
import websockets

from global_variables import CONNECTIONS
from messages import UserListMessage, UserLoginMessage, RegisterAttempt, LoginAttempt
from db.session import SessionLocal
from db.crud.auth import get_user_by_username, create_user
from db.crud.chat import get_chats_for_user
from typing import TypedDict, List

class SuccessResponse(TypedDict):
	status: str
	username: str
	chats: List[str]

class ErrorResponse(TypedDict):
	status: str
	error: str

Response = SuccessResponse | ErrorResponse

async def sendUserList(websocket):
	msg = UserListMessage(msg_type="user_list", users=list(CONNECTIONS.keys()))
	await websocket.send(json.dumps(msg.__dict__))

def broadcastConnectionsState(message_type, username):
	msg = UserLoginMessage(msg_type=message_type, username=username)
	websockets.broadcast(CONNECTIONS.values(), json.dumps(msg.__dict__))

async def register(register_attempt: RegisterAttempt) -> Response:
	with SessionLocal() as session:
		existing = get_user_by_username(session, register_attempt.username)
		if existing:
			return {
				"status": "error",
				"error": "Username already taken"
			}

		user = create_user(session, register_attempt.username, register_attempt.password)
		chats = get_chats_for_user(session, user.id)
		
		return {
			"status": "ok",
			"username": user.username,
			"chats": chats
		}

async def login(login_attempt: LoginAttempt) -> Response:
	# check credentials
	# query user chats
	pass
