from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer

from db.db import Base, chat_tablename, participant_tablename

class Chat(Base):
	__tablename__ = chat_tablename
	
	id = mapped_column(Integer, primary_key=True)

	task: Mapped["Task"] = relationship(back_populates="chat")
	participants: Mapped[List["User"]] = relationship(
		secondary=participant_tablename, back_populates="chats"
	)
	messages: Mapped[List["Message"]] = relationship(back_populates=chat_tablename)

	def __repr__(self) -> str:
		return f"Chat(id={self.id!r})"
