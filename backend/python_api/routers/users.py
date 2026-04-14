from typing import Literal, List, Annotated
from fastapi import HTTPException, status, APIRouter, Depends
from datetime import timedelta
from sqlalchemy.orm import Session

from db.session import get_session
from python_api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
    authenticate_user, get_password_hash, AuthRoute
)
from python_api.utils import validate_email, validate_password
from python_api.request_types import RegisterRequest, LoginRequest
from python_api.response_types import LoginResponse, UserResponse
from db.crud.task import TaskParticipant, get_task_participants
from db.crud.user import (
    get_all_users, create_user, get_user_by_username, get_user_by_email
)


unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)


@authenticated_router.get("/token")
def validate_token() -> Literal[True]:
    return True


@authenticated_router.get('/users', response_model=None)
def all_users(
    session: Annotated[Session, Depends(get_session)]
) -> List[UserResponse]:
    users = get_all_users(session)
    result = []
    for user in users:
        if not user.admin:
            result.append(UserResponse(id=user.id, name=user.username))
    return result


@authenticated_router.get('/task-participants', response_model=None)
def task_participants(
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
) -> List[TaskParticipant]:
    result = []
    for row in get_task_participants(session, task_id):
        if row[0].admin is False:
            result.append(TaskParticipant(
                id=row[0].id,
                name=row[0].username,
                role=row[1]
            ))

    return result


@unauthenticated_router.post("/register")
def register(
    data: RegisterRequest,
    session: Annotated[Session, Depends(get_session)]
) -> str:
    validate_email(data.email)
    validate_password(data.password)
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
    session.commit()
    return "Account successfully registered."


@unauthenticated_router.post("/login")
def login(
    data: LoginRequest,
    session: Annotated[Session, Depends(get_session)]
) -> LoginResponse:
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
    session.commit()
    return LoginResponse(
        username=user.username,
        access_token=access_token,
        user_id=user.id,
        is_admin=user.admin
    )


users_router = APIRouter()
users_router.include_router(authenticated_router)
users_router.include_router(unauthenticated_router)
