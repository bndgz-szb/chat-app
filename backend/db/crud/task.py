from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Literal
from dataclasses import dataclass
from db.models import Chat, Task, Topic, TaskTopic, User, ChatParticipant


@dataclass
class TaskParticipant():
    id: int
    name: str
    role: Literal['admin'] | Literal['guest'] | Literal['member']


def get_task_participants(
        session: Session, task_id: int
) -> List[TaskParticipant]:
    stmt = (
        select(User, ChatParticipant.role)
        .join(ChatParticipant)
        .join(Chat)
        .join(Task)
        .where(Task.id == task_id)
    )
    result = []
    for row in session.execute(stmt):
        result.append(TaskParticipant(
            id=row[0].id,
            name=row[0].username,
            role=row[1]
        ))

    return result


def get_tasks_with_topics(session: Session):
    return session.query(Task).all()


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    return session.query(Task).filter_by(id=task_id).first()


def create_task(
        session: Session, name: str, chat: Chat, creator: User,
        done: bool = False
) -> Task:
    task = Task(chat_id=chat.id, name=name, created_by=creator.id, done=done)
    session.add(task)
    session.commit()
    return task


def attach_topic(session: Session, task: Task, topic_id: int) -> None:
    # if task already has topic attached, nothing happens
    exists = session.query(TaskTopic).filter_by(
        task_id=task.id, topic_id=topic_id
    ).first()
    if exists == None:
        taskTopic = TaskTopic(task_id=task.id, topic_id=topic_id)
        session.add(taskTopic)
        session.commit()


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
