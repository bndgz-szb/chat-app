from datetime import datetime, timedelta

from db.models import ChatRole
from db.crud.chat import assign_user, create_chat
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
    assign_user(db_session, chat.id, admin_user.id, ChatRole.OWNER)
    db_session.commit()
    # task needed as well for the endpoint
    task = create_task(
        session=db_session,
        name="test",
        chat=chat,
        creator=admin_user,
        done=False
    )
    db_session.commit()

    response = test_client.get("/chat", headers=admin_header)
    chat_list = response.json()
    assert response.status_code == 200
    assert len(chat_list) == 1
    assert chat_list[0]["id"] == chat.id
    assert chat_list[0]["name"] == task.name


def test_message_history_unauth(test_client):
    response = test_client.get("/message-history")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_message_history_outsider(db_session, test_client, admin_header):
    chat = create_chat(db_session)
    db_session.commit()
    response = test_client.get(
        "/message-history",
        headers=admin_header,
        params={"chat_id": chat.id}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "User isn't part of chat"}


def test_message_history_owner(test_client, admin_header, db_session, admin_user):
    chat = create_chat(db_session)
    db_session.commit()
    assign_user(db_session, chat.id, admin_user.id, ChatRole.OWNER)
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    message_content = "test"
    send_message_to_chat(db_session, chat, admin_user, message_content, now)
    db_session.commit()

    response = test_client.get(
        "/message-history",
        headers=admin_header,
        params={"chat_id": chat.id}
    )
    messages = response.json()
    assert response.status_code == 200
    assert len(messages) == 1
    assert messages[0]["id"]
    assert messages[0]["chat_id"] == chat.id
    assert messages[0]["sender_id"] == admin_user.id
    assert messages[0]["content"] == message_content
    assert (messages[0]["sent_at"] == now.replace(" ", "T"))
    assert messages[0]["sender_username"] == admin_user.username


def test_message_history_guest(
    test_client, non_admin_header, db_session, admin_user, non_admin_user
):
    # send message before and after joining a guest
    seen_message, unseen_message = "test1", "test2"
    chat = create_chat(db_session)
    now = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d %H:%M:%S.%f')
    db_session.commit()
    assign_user(db_session, chat.id, admin_user.id, ChatRole.OWNER)
    send_message_to_chat(db_session, chat, admin_user, unseen_message, now)
    assign_user(db_session, chat.id, non_admin_user.id, ChatRole.GUEST)
    db_session.commit()
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    send_message_to_chat(db_session, chat, admin_user, seen_message, now)
    db_session.commit()

    response = test_client.get(
        "/message-history",
        headers=non_admin_header,
        params={"chat_id": chat.id}
    )
    messages = response.json()
    assert response.status_code == 200
    assert len(messages) == 1
    assert messages[0]["id"]
    assert messages[0]["chat_id"] == chat.id
    assert messages[0]["sender_id"] == admin_user.id
    assert messages[0]["content"] == seen_message
    assert messages[0]["sent_at"] == now.replace(" ", "T")
    assert messages[0]["sender_username"] == admin_user.username


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
    assert message["chat_id"] == chat.id
    assert message["sender_id"] == admin_user.id
    assert message["content"] == message_content
    assert message["sender_username"] == admin_user.username
