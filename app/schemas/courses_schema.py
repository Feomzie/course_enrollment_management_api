from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    code: str

class CourseUpdate(BaseModel):
    title: str
    code: str