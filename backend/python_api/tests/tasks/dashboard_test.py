from python_api.tests.tasks.utils import prep_task


def test_dashboard_zero(test_client):
    response = test_client.get("/dashboard")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 0


def test_dashboard_unauth(test_client, db_session, admin_user):
    task = prep_task("test", db_session, admin_user)
    response = test_client.get("/dashboard")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task.id
    assert tasks[0]["name"] == task.name
    assert tasks[0]["done"] == task.done
    assert tasks[0]["topics"] == task.topics
    assert tasks[0]["created_by"] == None
    assert tasks[0]["chat_id"] == None


def test_dashboard_auth(test_client, db_session, admin_user, admin_header):
    task = prep_task("test", db_session, admin_user)
    response = test_client.get("/dashboard", headers=admin_header)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task.id
    assert tasks[0]["name"] == task.name
    assert tasks[0]["done"] == task.done
    assert tasks[0]["topics"] == task.topics
    assert tasks[0]["created_by"] == task.created_by
    assert tasks[0]["chat_id"] == task.chat_id
