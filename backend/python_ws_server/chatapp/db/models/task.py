from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey

from chatapp.db.db import Base, task_tablename, chat_tablename, task_topic_tablename

class Task(Base):
	__tablename__ = task_tablename

	id = mapped_column(Integer, primary_key=True)
	chat_id = mapped_column(Integer, ForeignKey(f"{chat_tablename}.id"), nullable=False, unique=True)
	done = mapped_column(Boolean, default=False, nullable=False)

	chat: Mapped["Chat"] = relationship(back_populates="task", single_parent=True)
	topics: Mapped[List["Topic"]] = relationship(
		secondary=task_topic_tablename, back_populates="tasks"
	)

	def __repr__(self) -> str:
		return f"Task(id={self.id!r}, chat_id={self.chat_id!r}, done={self.done!r})"
