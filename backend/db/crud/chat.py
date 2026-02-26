from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from dataclasses import dataclass
from sqlalchemy import DateTime

from db.models import Chat, ChatParticipant, User, Task, Message


@dataclass
class ChatResponse:
    id: int
    name: str


@dataclass
class MessageWithUsername:
    id: int
    chat_id: int
    sender_id: int
    content: str
    sent_at: DateTime
    sender_username: str


def get_chat_by_id(session: Session, chat_id: int) -> Chat | None:
    return session.query(Chat).filter(Chat.id == chat_id).first()


def get_chats_for_user(
    session: Session, user_id: int
) -> List[ChatResponse]:
    stmt = (
        select(Chat.id, Task.name)
        .join(User.chats)
        .join(Chat.task)
        .where(User.id == user_id)
    )
    result = []
    for row in session.execute(stmt):
        result.append(ChatResponse(id=row[0], name=row[1]))

    return result


def get_messages_for_chat(
        session: Session, chat_id: int
) -> List[MessageWithUsername]:
    stmt = (
        select(Message, User.username)
        .join(Chat.messages)
        .join(Message.sender)
        .where(Chat.id == chat_id)
    )
    result = []
    for row in session.execute(stmt):
        result.append(MessageWithUsername(
            id=row[0].id,
            chat_id=row[0].chat_id,
            sender_id=row[0].sender_id,
            content=row[0].content,
            sent_at=row[0].sent_at,
            sender_username=row[1]
        ))
    return result


def create_chat(session: Session) -> Chat:
    chat = Chat()
    session.add(chat)
    session.commit()
    return chat


# if user is already assigned to chat, nothing happens
def assign_user(
    session: Session, chat: Chat, user: User, role: str = "member"
) -> None:
    exists = session.query(ChatParticipant).filter_by(
        chat_id=chat.id, user_id=user.id
    ).first()
    if exists == None:
        chatParticipant = ChatParticipant(
            chat_id=chat.id, user_id=user.id, role=role
        )
        session.add(chatParticipant)
        session.commit()
        session.refresh(chat)
        session.refresh(user)
