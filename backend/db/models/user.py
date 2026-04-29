from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean

from db.db import Base, user_tablename, participant_tablename


class User(Base):
    __tablename__ = user_tablename

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    email = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(254), nullable=False)  # hashed
    admin = mapped_column(Boolean, default=False, nullable=False)

    tasks: Mapped[List["Task"]] = relationship(back_populates="creator")
    chats: Mapped[List["Chat"]] = relationship(
        secondary=participant_tablename, back_populates="participants")
    messages: Mapped[List["Message"]] = relationship(back_populates="sender")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, username={self.username!r}, "
            f"email={self.email!r}, admin={self.admin!r})"
        )
