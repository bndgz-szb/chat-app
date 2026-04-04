from datetime import timedelta
from dataclasses import fields

from db.models import User
from db.crud.chat import create_chat, assign_user
from db.crud.task import create_task, TaskParticipant
from db.crud.message import send_message_to_chat
from db.crud.analytics import TaskWithAnalytics
from python_api.auth import (
    get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)


def test_analytics_unauth(test_client):
    response = test_client.get("/analytics")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_analytics_auth_non_admin(db_session, test_client):
    non_admin_user = User(
        username='test_non_admin',
        password=get_password_hash('test'),
        email='test_non_admin@example.com'
    )
    db_session.add(non_admin_user)
    db_session.commit()
    token = create_access_token(
        data={"sub": non_admin_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response = test_client.get(
        "/analytics", headers={"authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_analytics(db_session, user, test_client, prepare_auth_header):
    # create task with chat
    chat = create_chat(db_session)
    db_session.commit()
    for participant in [TaskParticipant(
        id=user.id,
        name=user.username,
        role="admin"
    )]:
        assign_user(db_session, chat.id, participant.id, participant.role)

    create_task(
        session=db_session,
        name="test",
        chat=chat,
        creator=user,
        done=False
    )
    db_session.commit()

    # send message
    send_message_to_chat(db_session, chat, user, "test")
    db_session.commit()

    response = test_client.get("/analytics", headers=prepare_auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 1
    for task_with_analytics in response.json():
        required = {f.name for f in fields(TaskWithAnalytics)}
        missing = required - task_with_analytics.keys()
        assert not missing, f"Missing keys: {missing}"
