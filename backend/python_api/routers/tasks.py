from fastapi import APIRouter, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session

from db.models import User
from db.session import get_session
from db.crud.chat import (
    get_chats_for_user, create_chat, assign_user, delete_chat
)
from db.crud.task import (
    get_tasks_with_topics, create_task,
    attach_topic, get_task_by_id, delete_task, update_task
)
from python_api.response_types import TaskWithTopic
from python_api.request_types import (
    CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest
)
from python_api.auth import (
    AuthRoute, get_current_user, credentials_exception
)
from python_api.utils import *


unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)


@unauthenticated_router.get("/dashboard", response_model=None)
def dashboard(
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> List[TaskWithTopic]:
    result = []
    if user is not None:
        chat_ids = list(
            map(lambda x: x.id, get_chats_for_user(session, user.id))
        )
    else:
        chat_ids = []
    tasks = get_tasks_with_topics(session)
    for task in tasks:
        result.append({
            "id": task.id,
            "name": task.name,
            "created_by": task.created_by if user is not None else None,
            "done": task.done,
            "topics": task.topics,
            "chat_id": task.chat_id if task.chat_id in chat_ids else None
        })
    return result


@authenticated_router.post('/create-task')
def create_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    request: CreateTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    validate_task_name(session, request)
    validate_task_topics(session, request)
    validate_task_participants(session, request)

    chat = create_chat(session)
    session.commit()
    for participant in request.participants:
        assign_user(session, chat.id, participant.id, participant.role)
    task = create_task(
        session=session,
        name=request.name,
        chat=chat,
        creator=user,
        done=request.done
    )
    session.commit()
    for topic in request.topics:
        attach_topic(session, task, topic.id)
    session.commit()

    return "Task created successfully"


@authenticated_router.delete('/delete-task')
def delete_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    request: DeleteTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    task = get_task_by_id(session, request.task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task with given id does not exist"
        )
    if not (user.admin or user.id == task.created_by):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to delete this task!"
        )
    delete_task(session, task)
    delete_chat(session, task.chat)
    session.commit()

    return "Task and its chat has been successfully deleted"


@authenticated_router.put('/update-task')
def update_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    request: UpdateTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    task = get_task_by_id(session, request.task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task with given id does not exist"
        )
    if not (user.admin or user.id == task.created_by):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to modify this task!"
        )

    if task.name != request.updated_task.name:
        validate_task_name(session, request.updated_task)
    validate_task_topics(session, request.updated_task)
    validate_task_participants(session, request.updated_task)
    update_task(
        session=session,
        task=task,
        updated_name=request.updated_task.name,
        updated_status=request.updated_task.done,
        updated_topic_ids=list(
            map(lambda topic: topic.id, request.updated_task.topics)
        ),
        updated_participants=request.updated_task.participants
    )
    session.commit()

    return "Task has been modified successfully"


tasks_router = APIRouter()
tasks_router.include_router(unauthenticated_router)
tasks_router.include_router(authenticated_router)
