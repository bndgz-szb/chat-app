from dataclasses import dataclass
from typing import Literal

@dataclass
class BaseMessage:
	msg_type: str
	message: str

@dataclass
class UserPresenceMessage:
	msg_type: str
	username: str

@dataclass
class UnicastMessage(BaseMessage):
	msg_type: Literal["message"]
	sender: str
	target: str

@dataclass
class BroadcastMessage(BaseMessage):
	msg_type: Literal["broadcast"]
	sender: str

@dataclass
class ErrorMessage(BaseMessage):
	msg_type: Literal["error"]

@dataclass
class UserListMessage:
	msg_type: Literal["user_list"]
	users: list[str]

@dataclass
class UserLoginMessage(UserPresenceMessage):
	msg_type: Literal["user_login"]

@dataclass
class UserLogoutMessage(UserPresenceMessage):
	msg_type: Literal["user_logout"]
