from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Literal
from dataclasses import dataclass

from db.models import Chat, ChatParticipant, User, Task, Message, ChatRole


@dataclass
class ChatResponse:
    id: int
    name: str


def get_chat_by_id(session: Session, chat_id: int) -> Chat | None:
    return session.scalar(
        select(Chat)
        .where(Chat.id == chat_id)
    )


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


def get_user_role_for_chat(
        session: Session, chat_id: int, user_id: int
) -> ChatRole | Literal[False]:
    role = session.scalar(
        select(ChatParticipant.role)
        .where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id
        )
    )
    if role is None:
        return False
    return role


def create_chat(session: Session) -> Chat:
    chat = Chat()
    session.add(chat)
    return chat


# if user is already assigned to chat, nothing happens
def assign_user(
    session: Session, chat_id: int,
    user_id: int, role: ChatRole = ChatRole.MEMBER
) -> None:
    exists = session.scalar(
        select(ChatParticipant)
        .where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id
        )
    )
    if exists == None:
        chat_participant = ChatParticipant(
            chat_id=chat_id, user_id=user_id, role=role
        )
        session.add(chat_participant)


def remove_user(
    session: Session, chat_id: int, user_id: int
) -> None:
    chat_participant = session.scalar(
        select(ChatParticipant)
        .where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id
        )
    )
    if chat_participant:
        session.delete(chat_participant)


def delete_chat(session: Session, chat: Chat) -> None:
    messages = session.scalars(
        select(Message)
        .where(Message.chat_id == chat.id)
    )
    for message in messages:
        session.delete(message)

    participants = session.scalars(
        select(ChatParticipant)
        .where(ChatParticipant.chat_id == chat.id)
    )
    for participant in participants:
        session.delete(participant)

    session.delete(chat)
