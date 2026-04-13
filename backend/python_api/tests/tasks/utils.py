from fastapi.testclient import TestClient
from httpx import Response
from typing import Dict

from db.models import Task, ChatRole
from db.crud import create_chat, create_task, assign_user


TASK_NAME = "test"


def prep_task(task_name, session, user) -> Task:
    chat = create_chat(session)
    session.commit()
    task = create_task(session, task_name, chat, user)
    assign_user(session, chat.id, user.id, ChatRole.OWNER)
    session.commit()
    return task


def prep_create_task_json(
    name, done, topic_id, topic_name, user_id, username, role
):
    return {
        "name": name,
        "done": done,
        "topics": (
            [{"id": topic_id, "name": topic_name}]
            if topic_id is not None
            else []
        ),
        "participants": (
            [{
                "id": user_id,
                "name": username,
                "role": role
            }]
            if user_id is not None
            else []
        )
    }


def prep_create_task_request(
    test_client: TestClient, header: Dict[str, str],
    user_id: int | None = None, username: str = "", done: bool = False,
    topic_name: str = "", topic_id: int | None = None,
    name: str = "test", role: str = ChatRole.OWNER.value
) -> Response:
    return test_client.post(
        "/create-task",
        headers=header,
        json=prep_create_task_json(
            name, done, topic_id, topic_name, user_id, username, role
        )
    )


def prep_update_task_request(
    test_client: TestClient, header: Dict[str, str], task_id: int,
    user_id: int | None = None, username: str = "", done: bool = False,
    topic_name: str = "", topic_id: int | None = None,
    name: str = TASK_NAME, role: str = ChatRole.OWNER.value
) -> Response:
    return test_client.put(
        url="/update-task",
        headers=header,
        json={
            "task_id": task_id,
            "updated_task": prep_create_task_json(
                name, done, topic_id, topic_name, user_id, username, role
            )
        }
    )
