from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Text, Boolean, ForeignKey, Integer, DateTime, func

class Base(DeclarativeBase):
	pass

class User(Base):
	__tablename__ = "user"

	id = mapped_column(Integer, primary_key=True)
	username = mapped_column(String(50), unique=True, nullable=False)
	password = mapped_column(String(50), nullable=False)  # hashed in real app
	last_seen = mapped_column(DateTime, default=func.now(), nullable=False)

	chats: Mapped[List["Chat"]] = relationship(
		secondary="chat_participant", back_populates="participants"
	)
	messages: Mapped[List["Message"]] = relationship(back_populates="sender")

	def __repr__(self) -> str:
		return f"User(id={self.id!r}, username={self.username!r}, last_seen={self.last_seen!r})"

class Chat(Base):
	__tablename__ = "chat"
	
	id = mapped_column(Integer, primary_key=True)
	name = mapped_column(String(100), nullable=True)
	is_group = mapped_column(Boolean, default=False, nullable=False)

	participants: Mapped[List["User"]] = relationship(
		secondary="chat_participant", back_populates="chats"
	)
	messages: Mapped[List["Message"]] = relationship(back_populates="chat")

	def __repr__(self) -> str:
		return f"Chat(id={self.id!r}, name={self.name!r}, is_group={self.is_group!r})"

class ChatParticipant(Base):
	__tablename__ = "chat_participant"

	chat_id = mapped_column(Integer, primary_key=True, ForeignKey("chats.id"))
	user_id = mapped_column(Integer, primary_key=True, ForeignKey("users.id"))
	role = mapped_column(String(20), default="member")
	joined_at = mapped_column(DateTime, default=func.now())

	def __repr__(self) -> str:
		return f"ChatParticipant(chat_id={self.chat_id!r}, user_id={self.user_id!r}, role={self.role!r}, joined_at={self.joined_at!r})"

class Message(Base):
	__tablename__ = "message"

	id = mapped_column(Integer, primary_key=True)
	chat_id = mapped_column(Integer, nullable=False, ForeignKey("chats.id"))
	sender_id = mapped_column(Integer, nullable=False, ForeignKey("users.id"))
	content = mapped_column(Text, nullable=False)
	sent_at = mapped_column(DateTime, default=func.now(), nullable=False)

	sender: Mapped[User] = relationship(back_populates="messages")
	chat: Mapped[Chat] = relationship(back_populates="messages")

	def __repr__(self) -> str:
		return f"Message(id={self.id!r}, chat_id={self.chat_id!r}, sender_id={self.sender_id!r}, content={self.content!r}, sent_at={self.sent_at!r})"

class Session(Base):
	# TODO
