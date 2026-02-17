from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from db.db import Base, topic_tablename, task_topic_tablename


class Topic(Base):
    __tablename__ = topic_tablename

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)

    tasks: Mapped[List["Task"]] = relationship(
        secondary=task_topic_tablename, back_populates="topics"
    )

    def __repr__(self) -> str:
        return f"Topic(id={self.id!r}, name={self.name!r})"
