
import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.courses import courses

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_courses():
    courses.clear()
    courses.extend([
        {"id": 1, "title": "Math", "code": "MTH101"},
        {"id": 2, "title": "Physics", "code": "PHY101"},
    ])


# GET /courses

def test_get_all_courses():
    response = client.get("/courses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


# GET /courses/{id}

def test_get_course_success():
    response = client.get("/courses/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Math"


def test_get_course_not_found():
    response = client.get("/courses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found."


# POST /courses

def test_create_course_success():
    payload = {
        "title": "Chemistry",
        "code": "CHM101"
    }

    response = client.post(
        "/courses?role=admin",
        json=payload
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["new_course"]["title"] == "Chemistry"


def test_create_course_duplicate_code():
    payload = {
        "title": "Advanced Math",
        "code": "MTH101"
    }

    response = client.post(
        "/courses?role=admin",
        json=payload
    )

    assert response.status_code == 400


def test_create_course_unauthorized():
    payload = {
        "title": "Chemistry",
        "code": "CHM101"
    }

    response = client.post(
        "/courses?role=student",
        json=payload
    )

    assert response.status_code == 401


# PUT /courses/{id}

def test_update_course_success():
    payload = {
        "title": "Advanced Math",
        "code": "MTH201"
    }

    response = client.put(
        "/courses/1?role=admin",
        json=payload
    )

    assert response.status_code == 200
    assert response.json()["updated_course"]["title"] == "Advanced Math"


def test_update_course_not_found():
    payload = {
        "title": "Unknown",
        "code": "UNK101"
    }

    response = client.put(
        "/courses/999?role=admin",
        json=payload
    )

    assert response.status_code == 404


def test_update_course_unauthorized():
    payload = {
        "title": "Hack",
        "code": "HCK101"
    }

    response = client.put(
        "/courses/1?role=student",
        json=payload
    )

    assert response.status_code == 401


# DELETE /courses/{id}

def test_delete_course_success():
    response = client.delete("/courses/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Course removed successfully"


def test_delete_course_not_found():
    response = client.delete("/courses/999")

    assert response.status_code == 404
