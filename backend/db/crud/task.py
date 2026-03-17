from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Literal
from dataclasses import dataclass
from db.models import Chat, Task, TaskTopic, User, ChatParticipant
from db.crud.chat import remove_user, assign_user


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
    return task


def attach_topic(session: Session, task: Task, topic_id: int) -> None:
    # if task already has topic attached, nothing happens
    exists = session.query(TaskTopic).filter_by(
        task_id=task.id, topic_id=topic_id
    ).first()
    if exists == None:
        task_topic = TaskTopic(task_id=task.id, topic_id=topic_id)
        session.add(task_topic)


def remove_topic(session: Session, task: Task, topic_id: int) -> None:
    # if task doesn't have topic attached, nothing happens
    task_topic = session.query(TaskTopic).filter_by(
        task_id=task.id, topic_id=topic_id
    ).first()
    if task_topic != None:
        session.delete(task_topic)


def update_task(
    session: Session, task: Task, updated_name: str, updated_status: bool,
    updated_topic_ids: List[int], updated_participants: List[TaskParticipant]
) -> None:
    task.name = updated_name
    task.done = updated_status

    # remove old topics
    old_topic_ids = session.scalars(
        select(TaskTopic.topic_id).where(TaskTopic.task_id == task.id)
    )
    for old_topic_id in old_topic_ids:
        if old_topic_id not in updated_topic_ids:
            remove_topic(session, task, old_topic_id)

    # attach new topics
    for new_topic_id in updated_topic_ids:
        if new_topic_id not in old_topic_ids:
            attach_topic(session, task, new_topic_id)

    # remove old participants
    old_participants = session.scalars(
        select(ChatParticipant)
        .where(ChatParticipant.chat_id == task.chat_id)
    ).all()
    old_participant_ids = list(
        map(
            lambda chat_participant: chat_participant.user_id,
            old_participants
        )
    )
    new_participant_ids = list(
        map(lambda user: user.id, updated_participants)
    )
    for old_participant in old_participants:
        if old_participant.user_id not in new_participant_ids:
            remove_user(session, task.chat_id, old_participant.user_id)
        else:
            # modify roles
            old_role = old_participant.role
            new_role = [new_participant.role
                        for new_participant in updated_participants
                        if new_participant.id == old_participant.user_id][0]
            if old_role != new_role:
                old_participant.role = new_role

    # assign new participants
    for new_participant in updated_participants:
        if new_participant.id not in old_participant_ids:
            assign_user(
                session, task.chat_id,
                new_participant.id, new_participant.role
            )


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
