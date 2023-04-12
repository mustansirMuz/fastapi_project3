from . import utils
from .client import client


def test_create_todo(test_db):
    response = utils.create_user_and_create_todo()
    assert response.json() == {"status": 201, "transaction": "Successful"}


def test_get_all_todos(test_db):
    utils.create_user_and_create_todo()

    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0] == utils.TEST_TODO


def test_get_todos_by_user(test_db):
    utils.create_user_and_create_todo()
    headers = utils.login_user_and_get_auth_header()

    response = client.get("/todos/user", headers=headers)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0] == utils.TEST_TODO


def test_get_todo_by_id(test_db):
    utils.create_user_and_create_todo()
    headers = utils.login_user_and_get_auth_header()

    response = client.get("/todos/1", headers=headers)
    assert response.status_code == 200
    todo = response.json()
    assert todo == utils.TEST_TODO


def test_update_todo(test_db):
    utils.create_user_and_create_todo()
    headers = utils.login_user_and_get_auth_header()

    updated_todo = utils.TEST_TODO.copy()
    updated_todo["title"] = "This is an updated title"
    response = client.put("/todos/1", json=updated_todo, headers=headers)

    assert response.status_code == 200

    response = client.get("/todos/1", headers=headers)
    todo = response.json()
    assert todo == updated_todo


def test_delete_todo(test_db):
    utils.create_user_and_create_todo()
    headers = utils.login_user_and_get_auth_header()

    response = client.delete("/todos/1", headers=headers)

    assert response.status_code == 200

    response = client.get("/todos")
    todos = response.json()
    assert len(todos) == 0
