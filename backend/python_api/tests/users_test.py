from sqlalchemy.orm import Session

from db.models import ChatRole, User
from db.crud.chat import create_chat, assign_user
from db.crud.task import create_task
from python_api.auth import get_password_hash
from python_api.tests.conftest import UNHASHED_TEST_USER_PASSWORD


def prep_user(session: Session, username: str, email: str, admin: bool) -> User:
    user = User(
        username=username,
        password=get_password_hash(UNHASHED_TEST_USER_PASSWORD),
        email=email,
        admin=admin
    )
    session.add(user)
    session.commit()
    return user


def test_token_unauth(test_client):
    response = test_client.get("/token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token(test_client, admin_header):
    response = test_client.get("/token", headers=admin_header)
    assert response.status_code == 200
    assert response.json() == True


def test_users_unauth(test_client):
    response = test_client.get("/users")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_users_no_admin_return(test_client, admin_header):
    response = test_client.get("/users", headers=admin_header)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 0


def test_users_one(test_client, non_admin_header, non_admin_user):
    response = test_client.get("/users", headers=non_admin_header)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["id"] == non_admin_user.id
    assert users[0]["name"] == non_admin_user.username


def test_users_two(db_session, test_client, non_admin_header, non_admin_user):
    # second user
    second_user = prep_user(db_session, "second", "second@test.com", False)
    response = test_client.get("/users", headers=non_admin_header)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    assert any(
        map(
            lambda x:
                x["id"] == second_user.id
                and x["name"] == second_user.username,
            users
        )
    )
    assert any(
        map(
            lambda x:
                x["id"] == non_admin_user.id
                and x["name"] == non_admin_user.username,
            users
        )
    )


def test_task_participants_unauth(test_client):
    response = test_client.get("/task-participants")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_task_participants(
    test_client, non_admin_header, db_session, non_admin_user
):
    chat = create_chat(db_session)
    db_session.commit()
    task = create_task(db_session, "test", chat, non_admin_user)
    db_session.commit()
    user_role = ChatRole.OWNER
    assign_user(db_session, chat.id, non_admin_user.id, user_role)
    db_session.commit()

    response = test_client.get(
        "/task-participants",
        headers=non_admin_header,
        params={"task_id": task.id}
    )
    assert response.status_code == 200
    particpants = response.json()
    assert len(particpants) == 1
    assert particpants[0]["id"] == non_admin_user.id
    assert particpants[0]["name"] == non_admin_user.username
    assert particpants[0]["role"] == user_role.value


def test_register_invalid_email(test_client, admin_user):
    response = test_client.post(
        "/register",
        json={
            "username": admin_user.username,
            "email": "invalid_email",
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Given email address is not a valid email address!"
    }


def test_register_invalid_password(test_client, admin_user):
    response = test_client.post(
        "/register",
        json={
            "username": admin_user.username,
            "email": f"new_{admin_user.email}",
            "password": "short"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Password has to be at least 8 characters long!"
    }


def test_register_taken_name(test_client, admin_user):
    response = test_client.post(
        "/register",
        json={
            "username": admin_user.username,
            "email": f"new_{admin_user.email}",
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}


def test_register_taken_email(test_client, admin_user):
    response = test_client.post(
        "/register",
        json={
            "username": f"new_{admin_user.username}",
            "email": admin_user.email,
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already taken"}


def test_register(test_client):
    response = test_client.post(
        "/register",
        json={
            "username": "test",
            "email": "test@example.com",
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 200
    assert response.json() == "Account successfully registered."


def test_login_incorrect_name(test_client, admin_user):
    response = test_client.post(
        "/login",
        json={
            "username": f"wrong_{admin_user.username}",
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    assert str.lower("WWW-Authenticate") in response.headers.keys()
    assert response.headers.get("WWW-Authenticate") == "Bearer"


def test_login_incorrect_password(test_client, admin_user):
    response = test_client.post(
        "/login",
        json={
            "username": admin_user.username,
            "password": f"wrong_{UNHASHED_TEST_USER_PASSWORD}"
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    assert str.lower("WWW-Authenticate") in response.headers.keys()
    assert response.headers.get("WWW-Authenticate") == "Bearer"


def test_login(test_client, admin_user):
    response = test_client.post(
        "/login",
        json={
            "username": admin_user.username,
            "password": UNHASHED_TEST_USER_PASSWORD
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json().keys()
    assert response.json()["username"] == admin_user.username
    assert response.json()["user_id"] == admin_user.id
    assert response.json()["is_admin"] == admin_user.admin
