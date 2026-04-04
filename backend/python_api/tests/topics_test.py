from sqlalchemy import inspect

from db.models import Topic
from db.crud.topic import create_topic
from db.crud.chat import create_chat
from db.crud.task import attach_topic, create_task


def test_topics_unauth(test_client):
    response = test_client.get("/topics")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_topics(test_client, prepare_auth_header, db_session):
    # create topic
    topic = create_topic(db_session, "test")
    db_session.commit()

    response = test_client.get("/topics", headers=prepare_auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 1
    for topic in response.json():
        required = inspect(Topic).c.keys()
        missing = required - topic.keys()
        assert not missing, f"Missing keys: {missing}"


def test_create_topic_unauth(test_client):
    response = test_client.post("/create-topic")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_create_topic(test_client, prepare_auth_header):
    response = test_client.post(
        "/create-topic",
        headers=prepare_auth_header,
        json={"name": "test"}
    )
    assert response.status_code == 200
    assert response.json() == "Topic created successfully"


def test_delete_topic_unauth(test_client):
    response = test_client.delete("/delete-topic")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_attached_topic(
    test_client, db_session, prepare_auth_header, user
):
    # create topic
    topic = create_topic(db_session, "test")
    db_session.commit()

    # create task
    chat = create_chat(db_session)  # needed for task creation
    db_session.commit()
    task = create_task(
        session=db_session,
        name="test",
        chat=chat,
        creator=user,
        done=False
    )
    db_session.commit()

    attach_topic(db_session, task, topic.id)
    db_session.commit()

    response = test_client.request(
        method="DELETE",
        url="/delete-topic",
        headers=prepare_auth_header,
        json={"topic_id": topic.id}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Could not delete topic."
                               " Make sure it is not attached to any tasks."}


def test_delete_topic(db_session, test_client, prepare_auth_header):
    # create topic
    topic = create_topic(db_session, "test")
    db_session.commit()

    response = test_client.request(
        method="DELETE",
        url="/delete-topic",
        headers=prepare_auth_header,
        json={"topic_id": topic.id}
    )
    assert response.status_code == 200
    assert response.json() == "Topic has been successfully deleted"
