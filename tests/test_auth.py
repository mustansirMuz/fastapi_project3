from fastapi import Response

from .client import client
from .utils import create_user, get_all_users, login_user


def test_create_user(test_db) -> None:
    response = create_user()
    assert response.status_code == 200

    response = get_all_users()
    assert response.status_code == 200
    assert response.json()[0]["username"] == "testuser"


def test_login_user(test_db) -> None:
    create_user()
    response = login_user()
    assert response.status_code == 200
    assert "token" in response.json()

    # incorrect credentials
    response = client.post(
        "auth/token",
        data={"username": "testuser", "password": "incorrect"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
