from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Sequence

from db.models import User


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.scalar(
        select(User)
        .where(User.username == username)
    )


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(
        select(User)
        .where(User.email == email)
    )


def get_all_users(session: Session) -> Sequence[User]:
    return session.scalars(select(User)).all()


def get_admin_user(session: Session) -> User | None:
    return session.scalar(select(User).where(User.admin == True))


def create_user(session: Session, username: str, email: str, hashed_password: str) -> User:
    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    return user
