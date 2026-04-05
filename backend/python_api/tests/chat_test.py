from dataclasses import fields

from db.crud.chat import (
    assign_user, create_chat, ChatResponse, MessageWithUsername
)
from db.crud.task import create_task
from db.crud.message import send_message_to_chat


def test_chat_unauth(test_client):
    response = test_client.get("/chat")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_chat(test_client, admin_header, admin_user, db_session):
    # assign user to a chat
    chat = create_chat(db_session)
    db_session.commit()
    assign_user(db_session, chat.id, admin_user.id, "admin")
    db_session.commit()
    # task needed as well for the endpoint
    create_task(
        session=db_session,
        name="test",
        chat=chat,
        creator=admin_user,
        done=False
    )
    db_session.commit()

    response = test_client.get("/chat", headers=admin_header)
    assert response.status_code == 200
    assert len(response.json()) == 1
    for chat in response.json():
        required = {f.name for f in fields(ChatResponse)}
        missing = required - chat.keys()
        assert not missing, f"Missing keys: {missing}"


def test_message_history_unauth(test_client):
    response = test_client.get("/message-history")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_message_history(test_client, admin_header, db_session, admin_user):
    chat = create_chat(db_session)
    db_session.commit()
    send_message_to_chat(db_session, chat, admin_user, "test")
    db_session.commit()

    response = test_client.get(
        "/message-history",
        headers=admin_header,
        params={"chat_id": chat.id}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    for message in response.json():
        required = {f.name for f in fields(MessageWithUsername)}
        missing = required - message.keys()
        assert not missing, f"Missing keys: {missing}"


def test_send_message_unauth(test_client):
    response = test_client.post("/message")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_send_message_fake_chat(
        test_client, admin_header, admin_user, admin_token
):
    response = test_client.post(
        "/message",
        headers=admin_header,
        json={
            "token": admin_token,
            "chat_id": -1,  # non-existent id
            "msg_type": "message",
            "sender_id": admin_user.id,
            "content": "test"
        })
    assert response.status_code == 400
    assert response.json() == {"detail": "Chat doesn't exist"}


def test_send_message(
    db_session, test_client, admin_header, admin_user, admin_token
):
    chat = create_chat(db_session)
    db_session.commit()

    message_content = "test"
    response = test_client.post(
        "/message",
        headers=admin_header,
        json={
            "token": admin_token,
            "chat_id": chat.id,
            "msg_type": "message",
            "sender_id": admin_user.id,
            "content": message_content
        })
    assert response.status_code == 200
    message = response.json()
    required = {f.name for f in fields(MessageWithUsername)}
    missing = required - message.keys()
    assert not missing, f"Missing keys: {missing}"
    assert message["chat_id"] == chat.id
    assert message["sender_id"] == admin_user.id
    assert message["content"] == message_content
    assert message["sender_username"] == admin_user.username
