from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey, String

from db.db import (
    Base, task_tablename, chat_tablename, task_topic_tablename, user_tablename
)


class Task(Base):
    __tablename__ = task_tablename

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), unique=True, nullable=False)
    chat_id = mapped_column(Integer, ForeignKey(
        f"{chat_tablename}.id"), nullable=False, unique=True)
    created_by = mapped_column(Integer, ForeignKey(
        f"{user_tablename}.id"), nullable=False)
    done = mapped_column(Boolean, default=False, nullable=False)

    creator: Mapped["User"] = relationship(back_populates="tasks")
    chat: Mapped["Chat"] = relationship(
        back_populates="task", single_parent=True)
    topics: Mapped[List["Topic"]] = relationship(
        secondary=task_topic_tablename, back_populates="tasks")

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, chat_id={self.chat_id!r}, "
            f"done={self.done!r})"
        )
