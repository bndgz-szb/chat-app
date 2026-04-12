from dataclasses import dataclass
from typing import Literal, List
from db.crud.message import MessageWithUsername


@dataclass
class ClientMessage:
    token: str
    chat_id: int


@dataclass
class HelloMessage(ClientMessage):
    msg_type: Literal["hello"]


@dataclass
class UnicastMessage(ClientMessage):
    msg_type: Literal["message"]
    sender_id: int
    content: str


@dataclass
class ErrorMessage:
    msg_type: Literal["error"]
    error: str


@dataclass
class HistoryMessage:
    msg_type: Literal["history"]
    messages: List[MessageWithUsername]
