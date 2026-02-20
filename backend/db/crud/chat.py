from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from db.models import Chat, ChatParticipant, User


def get_chats_for_user(session: Session, user_id: int) -> Sequence[str]:
    stmt = (
        select(Chat.id)
        .join(ChatParticipant)
        .where(ChatParticipant.user_id == user_id)
    )
    result = session.execute(stmt).scalars().all()
    return result


def create_chat(session: Session) -> Chat:
    chat = Chat()
    session.add(chat)
    session.commit()
    return chat


# if user is already assigned to chat, nothing happens
def assign_user(session: Session, chat: Chat, user: User, role: str = "member") -> None:
    exists = session.query(ChatParticipant).filter_by(
        chat_id=chat.id, user_id=user.id).first()
    if exists == None:
        chatParticipant = ChatParticipant(
            chat_id=chat.id, user_id=user.id, role=role)
        session.add(chatParticipant)
        session.commit()
        session.refresh(chat)
        session.refresh(user)
