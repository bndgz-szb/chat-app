from sqlalchemy.orm import Session
from sqlalchemy import select, func
from dataclasses import dataclass
from typing import List, Dict

from db.models import Message, Chat, Task, User


@dataclass
class MessagesByDay:
    day: str
    messages: int


@dataclass
class MessagesPerUser:
    username: str
    total_messages: int


@dataclass
class TaskWithAnalytics:
    name: str
    messagesByDays: List[MessagesByDay]
    messagesPerUsers: List[MessagesPerUser]


def get_task_analytics(session: Session) -> List[TaskWithAnalytics]:
    messages_by_days_raw = (
        select(
            Task.name,
            func.to_char(Message.sent_at, 'YYYY/MM/DD').label("day"),
            func.count(Message.id).label("messages")
        ).join(Message.chat)
        .join(Chat.task)
        .group_by(Task.name, "day")
    )
    messages_per_users_raw = (
        select(
            Task.name,
            User.username,
            func.count(Message.id).label("total_messages")
        ).join(Message.chat)
        .join(Chat.task)
        .join(Message.sender)
        .group_by(Task.name, User.username)
    )

    result: Dict[str, TaskWithAnalytics] = dict()
    for row in session.execute(messages_by_days_raw):
        task = result.get(row[0], TaskWithAnalytics(row[0], [], []))
        task.messagesByDays.append(MessagesByDay(row[1], row[2]))
        result[row[0]] = task
    for row in session.execute(messages_per_users_raw):
        task = result.get(row[0], TaskWithAnalytics(row[0], [], []))
        task.messagesPerUsers.append(MessagesPerUser(row[1], row[2]))
        result[row[0]] = task

    return list(result.values())
