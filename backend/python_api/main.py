from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Annotated, List, Tuple

from db.models import User
from db.crud.user import create_user, get_user_by_username, get_user_by_email
from db.crud.chat import get_chats_for_user, ChatResponse
from db.session import SessionLocal
from python_api.auth import (get_password_hash, create_access_token, Token,
                             ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                             RegisterRequest, LoginRequest, get_current_user
                             )
from python_api.auth import AuthRoute


app = FastAPI()

unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)

app.add_middleware(
    CORSMiddleware,
    # TODO use fix ip address of frontend
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Origin", "authorization"]
)


@unauthenticated_router.post("/register")
def register(data: RegisterRequest) -> str:
    with SessionLocal() as session:
        # check email validity
        # check password validity
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
def login(data: LoginRequest) -> Token:
    with SessionLocal() as session:
        user = authenticate_user(
            session, data.username, data.password)
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
        return Token(token_type="bearer", access_token=access_token)


@authenticated_router.get("/chat", response_model=None)
def chat(
    user: Annotated[User, Depends(get_current_user)]
) -> List[ChatResponse]:
    with SessionLocal() as session:
        return get_chats_for_user(session, user.id)


app.include_router(unauthenticated_router)
app.include_router(authenticated_router)
