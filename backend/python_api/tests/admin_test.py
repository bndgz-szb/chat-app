from dataclasses import fields

from db.models import ChatRole
from db.crud.chat import create_chat, assign_user
from db.crud.task import create_task, TaskParticipant
from db.crud.message import send_message_to_chat
from db.crud.analytics import TaskWithAnalytics


def test_analytics_unauth(test_client):
    response = test_client.get("/analytics")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_analytics_auth_non_admin(test_client, non_admin_header):
    response = test_client.get(
        "/analytics", headers={"authorization": f"Bearer {non_admin_header}"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_analytics(db_session, admin_user, test_client, admin_header):
    # create task with chat
    chat = create_chat(db_session)
    db_session.commit()
    for participant in [TaskParticipant(
        id=admin_user.id,
        name=admin_user.username,
        role=ChatRole.OWNER
    )]:
        assign_user(db_session, chat.id, participant.id, participant.role)

    create_task(
        session=db_session,
        name="test",
        chat=chat,
        creator=admin_user,
        done=False
    )
    db_session.commit()

    # send message
    send_message_to_chat(db_session, chat, admin_user, "test")
    db_session.commit()

    response = test_client.get("/analytics", headers=admin_header)
    assert response.status_code == 200
    assert len(response.json()) == 1
    for task_with_analytics in response.json():
        required = {f.name for f in fields(TaskWithAnalytics)}
        missing = required - task_with_analytics.keys()
        assert not missing, f"Missing keys: {missing}"
