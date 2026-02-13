from pydantic import BaseModel
from typing import Literal

class CourseCreate(BaseModel):
    role: Literal[
        "student", "admin"
    ]
    title: str
    code: str

class CourseUpdate(BaseModel):
    role: Literal[
        "student", "admin"
    ]
    title: str
    code: str