from sqlalchemy.orm import DeclarativeBase

user_tablename = "user"
chat_tablename = "chat"
participant_tablename = "chat_participant"
message_tablename = "message"
task_tablename = "task"
topic_tablename = "topic"
task_topic_tablename = "task_topic"


class Base(DeclarativeBase):
    pass
