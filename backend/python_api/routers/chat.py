from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated, List
from sqlalchemy.orm import Session

from db.models import User, ChatRole
from db.session import get_session
from db.crud.chat import (
    ChatResponse, get_chats_for_user,
    get_chat_by_id, get_user_role_for_chat, get_user_joined_at
)
from db.crud.message import (
    send_message_to_chat, MessageWithUsername, get_messages_for_chat
)
from python_api.auth import (
    AuthRoute, get_current_user, credentials_exception
)
from python_ws_server.chatapp.messages import UnicastMessage


unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)


# TODO fix response model
@authenticated_router.get("/chat", response_model=None, tags=["Chat"])
def chat(
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> List[ChatResponse]:
    if user is None:
        raise credentials_exception()
    return get_chats_for_user(session, user.id)


@authenticated_router.get("/message-history", response_model=None, tags=["Chat"])
def message_history(
    chat_id: int,
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> List[MessageWithUsername]:
    if user is None:
        raise credentials_exception()
    if chat_id == -1:
        return []
    messages = get_messages_for_chat(session, chat_id)
    user_role = get_user_role_for_chat(session, chat_id, user.id)
    if user_role is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User isn't part of chat"
        )

    if user_role is ChatRole.GUEST:
        start = get_user_joined_at(session, chat_id, user.id)
        if start is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User isn't part of chat"
            )
        messages = list(
            filter(lambda message: message.sent_at > start, messages)
        )
    return messages


@authenticated_router.post("/message", response_model=None, tags=["Chat"])
def send_message(
    message: UnicastMessage,
    user: Annotated[User | None, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> MessageWithUsername:
    if user is None:
        raise credentials_exception()
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


chat_router = APIRouter()
chat_router.include_router(unauthenticated_router)
chat_router.include_router(authenticated_router)
