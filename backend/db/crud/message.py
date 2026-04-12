from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Chat, User, Message


def send_message_to_chat(
        session: Session, chat: Chat, user: User, content: str,
        when: str = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
) -> Message:
    message = Message(
        chat_id=chat.id, sender_id=user.id, content=content, sent_at=when
    )
    session.add(message)
    return message
