import pytest
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


@pytest.fixture
def user() -> User:
    return User(
        username='test',
        password=get_password_hash('test'),
        email='test@example.com',
        admin=True
    )


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Create a new database session with a rollback at the end of the test.
    """
    # Create a SQLAlchemy engine
    engine = create_engine(
        "sqlite:///./test_db.db",
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
def prepare_auth_header(db_session, user) -> Dict[str, str]:
    db_session.add(user)
    db_session.commit()
    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"authorization": f"Bearer {token}"}
