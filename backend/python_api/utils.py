from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from python_api.request_types import CreateTaskRequest
from db.crud.task import get_task_by_name
from db.crud.user import get_all_users
from db.crud.topic import get_all_topics
from db.crud.chat import ChatRole


def validate_task_name(session: Session, task: CreateTaskRequest) -> None:
    exists = get_task_by_name(session, task.name)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Given task name is already taken!"
        )


def validate_task_topics(session: Session, task: CreateTaskRequest) -> None:
    all_topic_ids = list(
        map(lambda topic: topic.id, get_all_topics(session))
    )
    for topic in task.topics:
        if topic.id not in all_topic_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Given topic(s) are invalid!"
            )


def validate_task_participants(
    session: Session, task: CreateTaskRequest
) -> None:
    user_ids = list(map(lambda user: user.id, get_all_users(session)))
    for participant in task.participants:
        if participant.role not in ChatRole:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=("Invalid role provided for participant " +
                        participant.name)
            )
        if participant.id not in user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Given participant(s) are invalid!"
            )
