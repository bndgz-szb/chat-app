from sqlalchemy.orm import Session
from db.models import Chat, User, Message


def send_message_to_chat(session: Session, chat: Chat, user: User, content: str) -> None:
    message = Message(chat_id=chat.id, sender_id=user.id, content=content)
    session.add(message)
    session.commit()
    session.refresh(chat)
    session.refresh(user)
