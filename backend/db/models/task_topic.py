from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, ForeignKey

from db.db import Base, task_tablename, task_topic_tablename, topic_tablename

class TaskTopic(Base):
	__tablename__ = task_topic_tablename

	task_id = mapped_column(Integer, ForeignKey(f"{task_tablename}.id"), primary_key=True)
	topic_id = mapped_column(Integer, ForeignKey(f"{topic_tablename}.id"), primary_key=True)

	def __repr__(self) -> str:
		return f"TaskTopic(task_id={self.task_id!r}, topic_id={self.topic_id!r})"
