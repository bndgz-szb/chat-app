from python_api.tests.tasks.utils import prep_task


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
