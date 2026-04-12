from sqlalchemy.orm import Session
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import select
from typing import List

from db.models import Chat, User, Message


@dataclass
class MessageWithUsername:
    id: int
    chat_id: int
    sender_id: int
    content: str
    sent_at: datetime
    sender_username: str


def get_messages_for_chat(
        session: Session, chat_id: int
) -> List[MessageWithUsername]:
    stmt = (
        select(Message, User.username)
        .join(Chat.messages)
        .join(Message.sender)
        .where(Chat.id == chat_id)
        .order_by(Message.sent_at)
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


def send_message_to_chat(
        session: Session, chat: Chat, user: User,
        content: str, when: str | None = None
) -> Message:
    if when is None:
        when = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    message = Message(
        chat_id=chat.id, sender_id=user.id, content=content, sent_at=when
    )
    session.add(message)
    return message
