from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Tuple

from db.models import Chat, ChatParticipant, User, Task


class ChatResponse:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name


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
