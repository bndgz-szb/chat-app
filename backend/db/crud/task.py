from sqlalchemy.orm import Session
from sqlalchemy import select, Result
from typing import List, Sequence, Tuple
from dataclasses import dataclass
from db.models import Chat, Task, TaskTopic, User, ChatParticipant, ChatRole
from db.crud.chat import remove_user, assign_user
from db.crud.user import get_admin_user


@dataclass
class TaskParticipant():
    id: int
    name: str
    role: ChatRole


def get_task_participants(
        session: Session, task_id: int
) -> Result[Tuple[User, ChatRole]]:
    stmt = (
        select(User, ChatParticipant.role)
        .join(ChatParticipant)
        .join(Chat)
        .join(Task)
        .where(Task.id == task_id)
    )
    return session.execute(stmt)


def get_tasks_with_topics(session: Session) -> Sequence[Task]:
    return session.scalars(select(Task)).all()


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    return session.scalar(
        select(Task)
        .where(Task.id == task_id)
    )


def get_task_by_name(session: Session, task_name: str) -> Task | None:
    return session.scalar(
        select(Task)
        .where(Task.name == task_name)
    )


def create_task(
        session: Session, name: str, chat: Chat, creator: User,
        done: bool = False
) -> Task:
    task = Task(chat_id=chat.id, name=name, created_by=creator.id, done=done)
    session.add(task)
    return task


def attach_topic(session: Session, task: Task, topic_id: int) -> None:
    # if task already has topic attached, nothing happens
    exists = session.scalar(
        select(TaskTopic)
        .where(TaskTopic.task_id == task.id, TaskTopic.topic_id == topic_id)
    )
    if exists == None:
        task_topic = TaskTopic(task_id=task.id, topic_id=topic_id)
        session.add(task_topic)


def remove_topic(session: Session, task: Task, topic_id: int) -> None:
    # if task doesn't have topic attached, nothing happens
    task_topic = session.scalar(
        select(TaskTopic)
        .where(TaskTopic.task_id == task.id, TaskTopic.topic_id == topic_id)
    )
    if task_topic != None:
        session.delete(task_topic)


def update_task(
    session: Session, task: Task, updated_name: str, updated_status: bool,
    updated_topic_ids: List[int], updated_participants: List[TaskParticipant]
) -> None:
    task.name = updated_name
    task.done = updated_status

    update_task_topics(session, task, updated_topic_ids)

    admin = get_admin_user(session)
    admin_id = admin.id if admin else -1
    old_participants = session.scalars(
        select(ChatParticipant)
        .where(
            ChatParticipant.chat_id == task.chat_id,
            ChatParticipant.user_id != admin_id
        )
    ).all()
    remove_old_participants(
        session, task, updated_participants, old_participants
    )
    assign_new_participants(
        session, task, updated_participants, old_participants
    )


def update_task_topics(
    session: Session, task: Task, updated_topic_ids: List[int]
):
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


def remove_old_participants(
    session: Session, task: Task,
    updated_participants: List[TaskParticipant],
    old_participants: Sequence[ChatParticipant]
):
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


def assign_new_participants(
        session: Session, task: Task,
        updated_participants: List[TaskParticipant],
        old_participants: Sequence[ChatParticipant]
):
    old_participant_ids = list(
        map(
            lambda chat_participant: chat_participant.user_id,
            old_participants
        )
    )
    for new_participant in updated_participants:
        if new_participant.id not in old_participant_ids:
            assign_user(
                session, task.chat_id,
                new_participant.id, new_participant.role
            )


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
