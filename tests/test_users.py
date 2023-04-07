from .client import client
from .utils import (
    create_user,
    equals_test_user,
    get_all_users,
    login_user,
    login_user_and_get_auth_header,
)


def test_delete_user(test_db):
    create_user()
    headers = login_user_and_get_auth_header()
    response = client.delete("/users/", headers=headers)
    assert response.status_code == 200
    assert len(get_all_users().json()) == 0


def test_get_all_users(test_db):
    create_user()
    response = get_all_users()
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert equals_test_user(users[0])


def test_get_user_by_query(test_db):
    create_user()
    response = client.get("/users/user?user_id=1")
    assert response.status_code == 200
    assert equals_test_user(response.json())

    # wrong id
    response = client.get("/users/user?user_id=15")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_user_by_path(test_db):
    create_user()
    response = client.get("/users/1")
    assert response.status_code == 200
    assert equals_test_user(response.json())

    # wrong id
    response = client.get("/users/47")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_change_password(test_db):
    create_user()
    headers = login_user_and_get_auth_header()

    response = client.put(
        "/users/change_password",
        json={"new_password": "something_new"},
        headers=headers,
    )
    assert response.status_code == 200

    # check login with new password
    response = login_user("something_new")
    assert response.status_code == 200
    assert "token" in response.json()
