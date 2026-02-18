import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.users import users

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_users():
    users.clear()
    users.extend([
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "student"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "student"},
    ])


#POST /users

def test_create_user_success():
    data = {
        "name": "Charlie",
        "email": "charlie@example.com",
        "role": "admin"
    }

    response = client.post("/users", json=data)

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["new_user"]["name"] == "Charlie"
    assert body["new_user"]["email"] == "charlie@example.com"


#GET /users

def test_get_all_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


#GET /users/{id} (success)

def test_get_user_success():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


#GET /users/{id} (not found)

def test_get_user_not_found():
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"