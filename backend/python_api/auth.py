import os
import jwt
from typing import Literal
from pwdlib import PasswordHash
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from db.models import User
from db.crud.user import get_user_by_username

load_dotenv()
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if SECRET_KEY == None or ALGORITHM == None or ACCESS_TOKEN_EXPIRE_MINUTES == None:
    raise Exception("Don't forget to create .env file")
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)


class Token(BaseModel):
    token_type: str
    access_token: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
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


def authenticate_user(session: Session, username: str, password: str) -> User | Literal[False]:
    user = get_user_by_username(session=session, username=username)
    if not user:
        password_hash.verify(password, DUMMY_HASH)
        return False
    if not password_hash.verify(password, user.password):
        return False
    return user
