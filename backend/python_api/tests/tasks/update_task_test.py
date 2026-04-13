from db.models import ChatRole
from db.crud import create_topic
from db.crud.task import get_task_by_id, get_task_participants
from python_api.tests.tasks.utils import (
    prep_task, prep_update_task_request, TASK_NAME
)


def test_update_task_unauth(test_client):
    response = test_client.put("/update-task")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_update_task_fake_task(test_client, admin_header, admin_user):
    response = prep_update_task_request(
        test_client, admin_header, -1, admin_user.id, admin_user.username
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Task with given id does not exist"}


def test_update_task_non_updatable(
    db_session, test_client, non_admin_header, admin_user
):
    task = prep_task(TASK_NAME, db_session, admin_user)
    response = prep_update_task_request(
        test_client, non_admin_header, task.id,
        admin_user.id, admin_user.username
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
    response = prep_update_task_request(
        test_client, admin_header, task1.id, admin_user.id,
        admin_user.username, name=task2.name
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given task name is already taken!"}


def test_update_task_invalid_topic(
    test_client, admin_header, admin_user, db_session
):
    task = prep_task(TASK_NAME, db_session, admin_user)
    response = prep_update_task_request(
        test_client, admin_header, task.id, admin_user.id,
        admin_user.username, topic_id=-1, topic_name="i don't exist"
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given topic(s) are invalid!"}


def test_update_task_invalid_participant(
    test_client, admin_header, db_session, admin_user
):
    task = prep_task(TASK_NAME, db_session, admin_user)
    response = prep_update_task_request(
        test_client, admin_header, task.id, -1, "i_don't_exist"
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given participant(s) are invalid!"}


def test_update_task_zero_participant(
    test_client, admin_header, db_session, admin_user
):
    task = prep_task(TASK_NAME, db_session, admin_user)
    response = prep_update_task_request(
        test_client, admin_header, task.id
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "At least one participant is mandatory!"
    }


def test_update_task_name(test_client, admin_header, admin_user, db_session):
    task = prep_task("test1", db_session, admin_user)
    response = prep_update_task_request(
        test_client, admin_header, task.id, admin_user.id,
        admin_user.username, name="test2"
    )

    assert response.status_code == 200
    assert response.json() == "Task has been modified successfully"
    assert task.name == "test2"


def test_update_task_done(test_client, admin_header, admin_user, db_session):
    task = prep_task("test1", db_session, admin_user)
    response = prep_update_task_request(
        test_client, admin_header, task.id, admin_user.id,
        admin_user.username, True
    )

    assert response.status_code == 200
    assert response.json() == "Task has been modified successfully"
    assert task.done == True


def test_update_task_topics(
    test_client, admin_header, admin_user, db_session
):
    task = prep_task("test1", db_session, admin_user)
    topic = create_topic(db_session, "test")
    db_session.commit()
    response = prep_update_task_request(
        test_client, admin_header, task.id, admin_user.id,
        admin_user.username, topic_id=topic.id, topic_name=topic.name
    )
    task = get_task_by_id(db_session, task.id)

    assert response.status_code == 200
    assert response.json() == "Task has been modified successfully"
    assert task is not None
    assert len(task.topics) == 1
    assert task.topics[0].id == topic.id
    assert task.topics[0].name == topic.name


def test_update_task_participants(
    test_client, admin_header, admin_user, db_session, non_admin_user
):
    task = prep_task("test1", db_session, non_admin_user)
    db_session.commit()
    response = prep_update_task_request(
        test_client, admin_header, task.id,
        admin_user.id, admin_user.username, role=ChatRole.MEMBER.value
    )
    participants = get_task_participants(db_session, task.id).all()

    assert response.status_code == 200
    assert response.json() == "Task has been modified successfully"
    assert task is not None
    assert len(participants) == 1
    assert participants[0][0].id == admin_user.id
    assert participants[0][1] == ChatRole.MEMBER
