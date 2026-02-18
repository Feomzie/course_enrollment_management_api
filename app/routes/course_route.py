from fastapi import APIRouter, Depends, HTTPException
from app.schemas.courses_schema import CourseCreate, CourseUpdate
from app.schemas.enrollments_schema import AdminCheck
from app.models.courses import courses

router = APIRouter(tags=["Courses"])

@router.get("/courses")
def get_all_course():
    return courses


@router.get("/courses/{id}")
def get_course(id: int):
    for course in courses:
        if course["id"] == id:
            return course
    raise HTTPException(status_code=404, detail="Course not found.") 

    

@router.post("/courses")
def create_course(course_data: CourseCreate, admin_data:  AdminCheck = Depends ()):
    current_course_id = courses[-1]["id"] + 1

    if admin_data.role != "admin":
        raise HTTPException(status_code=401, detail="You are not an admin! Get out!") 
    for course in courses:
        if course["code"] == course_data.code:
            raise HTTPException(status_code=400, detail="Course code already.") 


    new_course = {
        "id": current_course_id,
        "title": course_data.title,
        "code": course_data.code,
    }

    courses.append(new_course)

    return {
        "status": "success",
        "new_course": new_course
    }


@router.put("/courses/{course_id}")
def update_course(course_id: int, course_data: CourseUpdate, admin_data:  AdminCheck = Depends ()):
    if admin_data.role != "admin":
        raise HTTPException(status_code=401, detail="You are not an admin! Get out!") 
    for course in courses:
        if course["id"] == course_id:
            if course_data.title is not None:
                course["title"] = course_data.title
            if course_data.code is not None:
                course["code"] = course_data.code
            return {
                "status": "success",
                "updated_course": course
            }

    raise HTTPException(status_code=404, detail="Course not found.") 


@router.delete("/courses/{id}")
def delete_course(id: int):
    for course in courses:
        if course["id"] == id:
            courses.remove(course)
            return {"message": "Course removed successfully"}
    raise HTTPException(status_code=404, detail="Course not found.") 