from pydantic import BaseModel
from typing import Literal

class EnrollmentCreate(BaseModel):
    role: Literal[
        "student", "admin"
    ]
    student_id: int
    course_id: int

class StudentCheck(BaseModel):
    role: Literal[
        "student", "admin"
    ]

class AdminCheck(BaseModel):
    role: Literal[
        "student", "admin"
    ]

class EnrollmentInfo(BaseModel):
    id: int
    student_id: int
    course_id: int