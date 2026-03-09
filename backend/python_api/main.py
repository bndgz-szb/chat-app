from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Annotated, List, Literal

from db.models import User, Topic
from db.crud.user import create_user, get_user_by_username, get_user_by_email
from db.crud.chat import (
    get_chats_for_user, ChatResponse, get_messages_for_chat,
    get_chat_by_id, MessageWithUsername
)
from db.crud.message import send_message_to_chat
from db.crud.task import get_tasks_with_topics
from db.crud.topic import get_all_topics
from db.session import SessionLocal
from python_api.auth import (
    get_password_hash, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
    get_current_user, credentials_exception
)
from python_api.request_types import RegisterRequest, LoginRequest
from python_api.response_types import LoginResponse, TaskWithTopic
from python_api.auth import AuthRoute
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
    with SessionLocal() as session:
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
        return MessageWithUsername(
            id=result.id,
            chat_id=result.chat_id,
            sender_id=result.sender_id,
            content=result.content,
            sent_at=result.sent_at,
            sender_username=user.username
        )


@authenticated_router.get('/topics', response_model=None)
def topics() -> List[Topic]:
    with SessionLocal() as session:
        return get_all_topics(session)


app.include_router(unauthenticated_router)
app.include_router(authenticated_router)
