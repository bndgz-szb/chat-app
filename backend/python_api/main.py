from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Annotated, List, Literal, Sequence
from sqlalchemy.orm import Session

from db.models import User, Topic
from db.crud.user import (
    create_user, get_user_by_username, get_user_by_email, get_all_users
)
from db.crud.chat import (
    get_chats_for_user, ChatResponse, get_messages_for_chat, delete_chat,
    get_chat_by_id, MessageWithUsername, create_chat, assign_user
)
from db.crud.message import send_message_to_chat
from db.crud.task import (
    get_tasks_with_topics, get_task_participants, update_task,
    TaskParticipant, create_task, attach_topic, get_task_by_id, delete_task
)
from db.crud.topic import get_all_topics, create_topic, delete_topic
from db.crud.analytics import get_task_analytics, TaskWithAnalytics
from db.session import SessionLocal
from python_api.auth import (
    get_password_hash, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
    get_current_user, credentials_exception, AuthRoute
)
from python_api.request_types import (
    RegisterRequest, LoginRequest, CreateTaskRequest, DeleteTopicRequest,
    DeleteTaskRequest, UpdateTaskRequest, CreateTopicRequest
)
from python_api.response_types import (
    LoginResponse, TaskWithTopic, UserResponse
)
from python_ws_server.chatapp.messages import UnicastMessage


app = FastAPI()

unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)

app.add_middleware(
    CORSMiddleware,
    # TODO use fix ip address of frontend
    allow_origins=["http://localhost:3000", "http://localhost:8765"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Origin", "authorization"]
)


@authenticated_router.get("/token")
def validate_token() -> Literal[True]:
    return True


@unauthenticated_router.post("/register")
def register(data: RegisterRequest) -> str:
    with SessionLocal.begin() as session:
        # TODO check email validity
        # TODO check password validity
        user = get_user_by_username(session, data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        user = get_user_by_email(session, data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )

        create_user(
            session=session, username=data.username, email=data.email,
            hashed_password=get_password_hash(data.password)
        )
        return "Account successfully registered."


@unauthenticated_router.post("/login")
def login(data: LoginRequest) -> LoginResponse:
    with SessionLocal() as session:
        user = authenticate_user(
            session, data.username, data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return LoginResponse(
            username=user.username,
            access_token=access_token,
            user_id=user.id,
            is_admin=user.admin
        )


@unauthenticated_router.get("/dashboard", response_model=None)
def dashboard(
    user: Annotated[User | None, Depends(get_current_user)]
) -> List[TaskWithTopic]:
    with SessionLocal() as session:
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


# TODO fix response model
@authenticated_router.get("/chat", response_model=None)
def chat(
    user: Annotated[User | None, Depends(get_current_user)]
) -> List[ChatResponse]:
    if user is None:
        raise credentials_exception()
    with SessionLocal() as session:
        return get_chats_for_user(session, user.id)


@authenticated_router.get("/message-history", response_model=None)
def message_history(chat_id: int) -> List[MessageWithUsername]:
    with SessionLocal() as session:
        return get_messages_for_chat(session, chat_id)


@authenticated_router.post("/message", response_model=None)
def send_message(
    message: UnicastMessage,
    user: Annotated[User | None, Depends(get_current_user)]
) -> MessageWithUsername:
    if user is None:
        raise credentials_exception()
    with SessionLocal() as session:
        chat = get_chat_by_id(session, message.chat_id)
        if chat is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat doesn't exist"
            )
        result = send_message_to_chat(session, chat, user, message.content)
        session.commit()
        return MessageWithUsername(
            id=result.id,
            chat_id=result.chat_id,
            sender_id=result.sender_id,
            content=result.content,
            sent_at=result.sent_at,
            sender_username=user.username
        )


@authenticated_router.get('/topics', response_model=None)
def topics() -> Sequence[Topic]:
    with SessionLocal() as session:
        return get_all_topics(session)


@authenticated_router.get('/users', response_model=None)
def all_users() -> List[UserResponse]:
    with SessionLocal() as session:
        users = get_all_users(session)
        result = []
        for user in users:
            result.append(UserResponse(id=user.id, name=user.username))
        return result


@authenticated_router.get('/task-participants', response_model=None)
def task_participants(task_id: int) -> List[TaskParticipant]:
    with SessionLocal() as session:
        return get_task_participants(session, task_id)


@authenticated_router.post('/create-task')
def create_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    request: CreateTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    with SessionLocal() as session:
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


@authenticated_router.post('/create-topic')
def create_topic_endpoint(request: CreateTopicRequest) -> str:
    with SessionLocal.begin() as session:
        create_topic(session, request.name)
    return "Topic created successfully"


@authenticated_router.delete('/delete-task')
def delete_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    request: DeleteTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    with SessionLocal.begin() as session:
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

    return "Task and its chat has been successfully deleted"


@authenticated_router.delete('/delete-topic')
def delete_topic_endpoint(request: DeleteTopicRequest) -> str:
    with SessionLocal.begin() as session:
        isDeleteSuccess = delete_topic(session, request.topic_id)
    if isDeleteSuccess:
        return "Topic has been successfully deleted"
    else:
        return ("Could not delete topic."
                " Make sure it is not attached to any tasks")


@authenticated_router.put('/update-task')
def update_task_endpoint(
    user: Annotated[User | None, Depends(get_current_user)],
    request: UpdateTaskRequest
) -> str:
    if user is None:
        raise credentials_exception()
    with SessionLocal.begin() as session:
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

    return "Task has been modified successfully"


@authenticated_router.get('/analytics')
def get_analytics(
    user: Annotated[User | None, Depends(get_current_user)]
) -> List[TaskWithAnalytics]:
    if user is None or not user.admin:
        raise credentials_exception()
    with SessionLocal() as session:
        return get_task_analytics(session)


app.include_router(unauthenticated_router)
app.include_router(authenticated_router)


def validate_task_topics(
    session: Session, task: CreateTaskRequest
) -> None:
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
        if participant.id not in user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Given participant(s) are invalid!"
            )
