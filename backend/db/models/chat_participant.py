import datetime
import enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, DateTime, func

from db.db import Base, participant_tablename, chat_tablename, user_tablename


class ChatRole(enum.Enum):
    OWNER = "owner"
    MEMBER = "member"
    GUEST = "guest"


class ChatParticipant(Base):
    __tablename__ = participant_tablename

    chat_id = mapped_column(Integer, ForeignKey(
        f"{chat_tablename}.id"), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(
        f"{user_tablename}.id"), primary_key=True)
    role: Mapped[ChatRole] = mapped_column(
        SAEnum(ChatRole), default="member", nullable=False
    )
    joined_at = mapped_column(DateTime, default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"ChatParticipant(chat_id={self.chat_id!r}, user_id={self.user_id!r}, role={self.role!r}, joined_at={self.joined_at!r})"
