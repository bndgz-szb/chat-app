import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, StaticPool
from datetime import timedelta
from typing import Dict, Generator

from db.db import Base
from db.session import get_session
from db.models import User
from python_api.main import app
from python_api.auth import (
    get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)


DB_TEST_URL = os.getenv("DB_TEST_URL")
UNHASHED_TEST_USER_PASSWORD = "test"


@pytest.fixture
def admin_user(db_session) -> User:
    user = User(
        username='test_admin',
        password=get_password_hash(UNHASHED_TEST_USER_PASSWORD),
        email='test_admin@example.com',
        admin=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def non_admin_user(db_session) -> User:
    user = User(
        username='test_non_admin',
        password=get_password_hash(UNHASHED_TEST_USER_PASSWORD),
        email='test_non_admin@example.com',
        admin=False
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Create a new database session with a rollback at the end of the test.
    """

    # Create a SQLAlchemy engine
    if DB_TEST_URL == None:
        raise Exception("Don't forget to create .env file with DB_TEST_URL")
    engine = create_engine(
        DB_TEST_URL,
        poolclass=StaticPool,
    )

    # Create a sessionmaker to manage sessions
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False
    )

    # Create tables in the database
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(db_session) -> Generator[TestClient, None, None]:
    """
    Create a test client that uses the
    override_get_session fixture to return a session.
    """

    def override_get_session():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(admin_user) -> str:
    return create_access_token(
        data={"sub": admin_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


@pytest.fixture
def non_admin_token(non_admin_user) -> str:
    return create_access_token(
        data={"sub": non_admin_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


@pytest.fixture
def admin_header(admin_token) -> Dict[str, str]:
    return {"authorization": f"Bearer {admin_token}"}


@pytest.fixture
def non_admin_header(non_admin_token) -> Dict[str, str]:
    return {"authorization": f"Bearer {non_admin_token}"}
