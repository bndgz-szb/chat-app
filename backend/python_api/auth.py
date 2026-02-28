import os
import jwt
from typing import Literal, Annotated, Any, Callable
from pwdlib import PasswordHash
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRoute
from collections.abc import Coroutine

from db.models import User
from db.crud.user import get_user_by_username
from db.session import SessionLocal

load_dotenv()
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if (SECRET_KEY == None or ALGORITHM == None
        or ACCESS_TOKEN_EXPIRE_MINUTES == None):
    raise Exception("Don't forget to create .env file")
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)


class TokenData(BaseModel):
    username: str


class AuthScheme():
    def __call__(self, request: Request) -> str:
        authorization = request.headers.get("Authorization")
        if not authorization:
            scheme, param = "", ""
        else:
            scheme, _, param = authorization.partition(" ")
            param = param.strip()
        if not authorization or scheme.lower() != "bearer":
            return ""
        return param


class AuthRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                token = auth_scheme(request)
                payload = jwt.decode(
                    token, SECRET_KEY, algorithms=[str(ALGORITHM)]
                )
                username = payload.get("sub")
                if username is None:
                    raise credentials_exception()
            except InvalidTokenError:
                raise credentials_exception()

            response = await original_route_handler(request)
            return response

        return custom_route_handler


auth_scheme = AuthScheme()


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def authenticate_user(
    session: Session, username: str, password: str
) -> User | Literal[False]:
    user = get_user_by_username(session=session, username=username)
    if not user:
        password_hash.verify(password, DUMMY_HASH)
        return False
    if not password_hash.verify(password, user.password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(auth_scheme)]
) -> User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[str(ALGORITHM)])
        username = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except InvalidTokenError:
        return None
    with SessionLocal() as session:
        user = get_user_by_username(session, token_data.username)
        return user
