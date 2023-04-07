from fastapi import Response

from .client import client

TEST_USER = {
    "username": "testuser",
    "email": "testuser@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "12345678",
    "phone_number": "+921234212345",
}

TEST_TODO = {
    "id": 1,
    "title": "This is a test todo",
    "description": "Testing is important",
    "priority": 3,
    "complete": False,
    "owner_id": 1,
}


def create_user() -> Response:
    return client.post("/auth/create/user", json=TEST_USER)


def login_user(password="12345678") -> Response:
    auth = {"username": "testuser", "password": password}
    return client.post("/auth/token", data=auth)


def login_user_and_get_auth_header() -> dict:
    response = login_user()
    token = response.json().get("token")
    return {"Authorization": f"Bearer {token}"}


def get_all_users() -> Response:
    return client.get("/users")


def equals_test_user(user: dict) -> bool:
    fields_to_check = ["username", "email", "first_name", "last_name"]
    for field in fields_to_check:
        if user[field] != TEST_USER[field]:
            return False
    return True


def create_todo(headers: dict, todo: dict = TEST_TODO) -> Response:
    return client.post("/todos/", json=todo, headers=headers)


def create_user_and_create_todo():
    create_user()
    headers = login_user_and_get_auth_header()
    return create_todo(headers)
