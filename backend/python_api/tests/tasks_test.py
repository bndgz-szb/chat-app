from dataclasses import fields

from db.models import Task
from db.crud.task import create_task
from db.crud.chat import create_chat
from python_api.response_types import TaskWithTopic


def prep_task(task_name, session, user) -> Task:
    chat = create_chat(session)
    session.commit()
    task = create_task(session, task_name, chat, user)
    session.commit()
    return task


def test_dashboard(test_client, db_session, admin_user):
    prep_task("test", db_session, admin_user)
    response = test_client.get("/dashboard")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    for task in tasks:
        required = {f.name for f in fields(TaskWithTopic)}
        missing = required - task.keys()
        assert not missing, f"Missing keys: {missing}"


def test_create_task_unauth(test_client):
    response = test_client.post("/create-task")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_create_task_duplicate_name(
        test_client, db_session, admin_header, admin_user
):
    task = prep_task("test", db_session, admin_user)
    response = test_client.post(
        "/create-task",
        headers=admin_header,
        json={
            "name": task.name,
            "done": False,
            "topics": [],
            "participants": [{
                "id": admin_user.id,
                "name": admin_user.username,
                "role": "admin"
            }]
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Given task name is already taken!"}


def test_create_task_invalid_topic(test_client, admin_header, admin_user):
    response = test_client.post(
        "/create-task",
        headers=admin_header,
        json={
            "name": "test",
            "done": False,
            "topics": [{"id": 1, "name": "i_don't_exist"}],
            "participants": [{
                "id": admin_user.id,
                "name": admin_user.username,
                "role": "admin"
            }]
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given topic(s) are invalid!"}


def test_create_task_invalid_participant(
        test_client, admin_header
):
    response = test_client.post(
        "/create-task",
        headers=admin_header,
        json={
            "name": "test",
            "done": False,
            "topics": [],
            "participants": [{
                "id": -1,
                "name": "i_don't_exist",
                "role": "admin"
            }]
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given participant(s) are invalid!"}


def test_create_task(test_client, admin_header, admin_user):
    response = test_client.post(
        "/create-task",
        headers=admin_header,
        json={
            "name": "test",
            "done": False,
            "topics": [],
            "participants": [{
                "id": admin_user.id,
                "name": admin_user.username,
                "role": "admin"
            }]
        }
    )

    assert response.status_code == 200
    assert response.json() == "Task created successfully"


def test_delete_task_unauth(test_client):
    response = test_client.delete("/delete-task")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_task_fake_task(test_client, admin_header):
    response = test_client.request(
        method="DELETE",
        url="/delete-task",
        headers=admin_header,
        json={"task_id": -1}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Task with given id does not exist"}


def test_delete_task_non_deletable(
        db_session, test_client, non_admin_header, admin_user
):
    # create task
    task = prep_task("test", db_session, admin_user)
    response = test_client.request(
        method="DELETE",
        url="/delete-task",
        headers=non_admin_header,
        json={"task_id": task.id}
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You don't have permission to delete this task!"
    }


def test_delete_task(db_session, test_client, admin_user, admin_header):
    task = prep_task("test", db_session, admin_user)
    response = test_client.request(
        method="DELETE",
        url="/delete-task",
        headers=admin_header,
        json={
            "task_id": task.id
        }
    )
    assert response.status_code == 200
    assert (
        response.json() == "Task and its chat has been successfully deleted"
    )


def test_update_task_unauth(test_client):
    response = test_client.put("/update-task")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_update_task_fake_task(test_client, admin_header, admin_user):
    response = test_client.put(
        url="/update-task",
        headers=admin_header,
        json={
            "task_id": -1,
            "updated_task": {
                "name": "test",
                "done": False,
                "topics": [],
                "participants": [{
                    "id": admin_user.id,
                    "name": admin_user.username,
                    "role": "admin"
                }]
            }
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Task with given id does not exist"}


def test_update_task_non_updatable(
        db_session, test_client, non_admin_header, admin_user
):
    task = prep_task("test", db_session, admin_user)
    response = test_client.put(
        url="/update-task",
        headers=non_admin_header,
        json={
            "task_id": task.id,
            "updated_task": {
                "name": "test",
                "done": False,
                "topics": [],
                "participants": [{
                    "id": admin_user.id,
                    "name": admin_user.username,
                    "role": "admin"
                }]
            }
        }
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You don't have permission to modify this task!"
    }


def test_update_task_duplicate_name(
        test_client, db_session, admin_header, admin_user
):
    task1 = prep_task("test1", db_session, admin_user)
    task2 = prep_task("test2", db_session, admin_user)
    response = test_client.put(
        "/update-task",
        headers=admin_header,
        json={
            "task_id": task1.id,
            "updated_task": {
                "name": task2.name,
                "done": False,
                "topics": [],
                "participants": [{
                    "id": admin_user.id,
                    "name": admin_user.username,
                    "role": "admin"
                }]
            }
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Given task name is already taken!"}


def test_update_task_invalid_topic(
    test_client, admin_header, admin_user, db_session
):
    task = prep_task("test", db_session, admin_user)
    response = test_client.put(
        "/update-task",
        headers=admin_header,
        json={
            "task_id": task.id,
            "updated_task": {
                "name": "test",
                "done": False,
                "topics": [{"id": -1, "name": "i don't exist"}],
                "participants": [{
                    "id": admin_user.id,
                    "name": admin_user.username,
                    "role": "admin"
                }]
            }
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given topic(s) are invalid!"}


def test_update_task_invalid_participant(
        test_client, admin_header, db_session, admin_user
):
    task = prep_task("test", db_session, admin_user)
    response = test_client.put(
        "/update-task",
        headers=admin_header,
        json={
            "task_id": task.id,
            "updated_task": {
                "name": "test",
                "done": False,
                "topics": [],
                "participants": [{
                    "id": -1,
                    "name": "i_don't_exist",
                    "role": "admin"
                }]
            }
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given participant(s) are invalid!"}


def test_update_task(test_client, admin_header, admin_user, db_session):
    task = prep_task("test1", db_session, admin_user)
    response = test_client.put(
        "update-task",
        headers=admin_header,
        json={
            "task_id": task.id,
            "updated_task": {
                "name": "test2",
                "done": False,
                "topics": [],
                "participants": [{
                    "id": admin_user.id,
                    "name": admin_user.username,
                    "role": "admin"
                }]
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == "Task has been modified successfully"
