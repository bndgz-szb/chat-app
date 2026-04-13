from db.models import ChatRole
from db.crud import create_topic
from db.crud.task import get_task_by_name, get_task_participants
from python_api.tests.tasks.utils import (
    prep_task, prep_create_task_request, TASK_NAME
)


def test_create_task_unauth(test_client):
    response = test_client.post("/create-task")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_create_task_duplicate_name(
        test_client, db_session, admin_header, admin_user
):
    prep_task(TASK_NAME, db_session, admin_user)
    response = prep_create_task_request(
        test_client, admin_header, admin_user.id,
        admin_user.username, name=TASK_NAME
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Given task name is already taken!"}


def test_create_task_invalid_topic(test_client, admin_header, admin_user):
    response = prep_create_task_request(
        test_client, admin_header, admin_user.id, admin_user.username,
        topic_id=-1, topic_name="i_don't_exist"
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given topic(s) are invalid!"}


def test_create_task_invalid_participant(
        test_client, admin_header
):
    response = prep_create_task_request(
        test_client, admin_header, -1, "i_don't_exist"
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Given participant(s) are invalid!"}


def test_create_task_zero_participant(
    test_client, admin_header
):
    response = prep_create_task_request(test_client, admin_header)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "At least one participant is mandatory!"
    }


def test_create_task(db_session, test_client, admin_header, admin_user):
    response = prep_create_task_request(
        test_client, admin_header, admin_user.id, admin_user.username
    )
    task = get_task_by_name(db_session, TASK_NAME)
    assert task is not None
    participants = get_task_participants(db_session, task.id).all()
    assert task is not None

    assert response.status_code == 200
    assert response.json() == "Task created successfully"
    assert task.id
    assert task.chat_id
    assert task.created_by == admin_user.id
    assert task.done == False
    assert task.name == TASK_NAME
    assert len(task.topics) == 0
    assert len(participants) == 1
    assert participants[0][0].id == admin_user.id
    assert participants[0][1] == ChatRole.OWNER


def test_create_done_task(db_session, test_client, admin_header, admin_user):
    response = prep_create_task_request(
        test_client, admin_header, admin_user.id, admin_user.username, True
    )

    assert response.status_code == 200
    assert response.json() == "Task created successfully"
    task = get_task_by_name(db_session, TASK_NAME)
    assert task is not None
    assert task.id
    assert task.chat_id
    assert task.created_by == admin_user.id
    assert task.done == True
    assert task.name == TASK_NAME
    assert len(task.topics) == 0


def test_create_task_with_topic(
    db_session, test_client, admin_header, admin_user
):
    topic = create_topic(db_session, "test")
    db_session.commit()
    response = prep_create_task_request(
        test_client, admin_header, admin_user.id, admin_user.username,
        topic_id=topic.id, topic_name=topic.name
    )

    assert response.status_code == 200
    assert response.json() == "Task created successfully"
    task = get_task_by_name(db_session, TASK_NAME)
    assert task is not None
    assert task.id
    assert task.chat_id
    assert task.created_by == admin_user.id
    assert task.done == False
    assert task.name == TASK_NAME
    assert len(task.topics) == 1
    assert task.topics[0].name == topic.name
    assert task.topics[0].id == topic.id
