import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, Integer, DateTime, func

from db.db import Base, message_tablename, chat_tablename, user_tablename


class Message(Base):
    __tablename__ = message_tablename

    id = mapped_column(Integer, primary_key=True)
    chat_id = mapped_column(Integer, ForeignKey(
        f"{chat_tablename}.id"), nullable=False)
    sender_id = mapped_column(Integer, ForeignKey(
        f"{user_tablename}.id"), nullable=False)
    content = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    sender: Mapped["User"] = relationship(back_populates="messages")
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return (
            f"Message(id={self.id!r}, chat_id={self.chat_id!r}, "
            f"sender_id={self.sender_id!r}, content={self.content!r}, "
            f"sent_at={self.sent_at!r})"
        )
