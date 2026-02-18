import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.enrollments import enrollments

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_enrollments():
    enrollments.clear()
    enrollments.extend([
        {"id": 1, "student_id": 1, "course_id": 1},
        {"id": 2, "student_id": 2, "course_id": 2},
    ])


# POST /enrollments

def test_enroll_student_success():
    payload = {
        "role": "student",
        "student_id": 1,
        "course_id": 2
    }

    response = client.post(
        "/enrollments?role=student",
        json=payload
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["new_enrollment"]["student_id"] == 1
    assert body["new_enrollment"]["course_id"] == 2


def test_enroll_student_duplicate():
    payload = {
        "role": "student",
        "student_id": 1,
        "course_id": 1
    }

    response = client.post(
        "/enrollments?role=student",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already enrolled this course."


def test_enroll_student_wrong_role():
    payload = {
        "role": "admin",
        "student_id": 1,
        "course_id": 2
    }

    response = client.post(
        "/enrollments?role=admin",
        json=payload
    )

    assert response.status_code == 401


# DELETE /enrollments/deregister/{id}

def test_student_deregister_success():
    response = client.delete(
        "/enrollments/deregister/1?role=student"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_student_deregister_not_found():
    response = client.delete(
        "/enrollments/deregister/999?role=student"
    )

    assert response.status_code == 404


# GET /admin/enrollments

def test_admin_get_all_enrollments():
    response = client.get(
        "/admin/enrollments?role=admin"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_get_all_enrollments_unauthorized():
    response = client.get(
        "/admin/enrollments?role=student"
    )

    assert response.status_code == 401


# GET /admin/enrollment/{course_id}

def test_admin_get_enrollment_success():
    response = client.get(
        "/admin/enrollment/1?role=admin"
    )

    assert response.status_code == 200
    assert response.json()["course_id"] == 1


def test_admin_get_enrollment_not_found():
    response = client.get(
        "/admin/enrollment/999?role=admin"
    )

    assert response.status_code == 404


# DELETE /admin/force-deregister/{id}

def test_admin_force_deregister_success():
    response = client.delete(
        "/admin/force-deregister/1?role=admin"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_admin_force_deregister_unauthorized():
    response = client.delete(
        "/admin/force-deregister/1?role=student"
    )

    assert response.status_code == 401