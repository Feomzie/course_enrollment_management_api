from fastapi import APIRouter, Depends, HTTPException
from app.schemas.enrollments_schema import EnrollmentCreate, StudentCheck, AdminCheck, EnrollmentInfo
from app.models.enrollments import enrollments

router = APIRouter(tags=["Enrollments"])

@router.post("/enrollments")
def enroll_student(enrollment_data: EnrollmentCreate, student_data:  StudentCheck = Depends ()):
    enrollment_id = enrollments[-1]["id"] + 1

    if student_data.role != "student":
        raise HTTPException(status_code=401, detail="You are not a student! Get out!")
    
    student_exists = False
    course_exists = False

    for enrollment in enrollments:
        if enrollment["student_id"] == enrollment_data.student_id and enrollment["course_id"] == enrollment_data.course_id:
            raise HTTPException(status_code=400, detail="Student already enrolled this course.")
        if enrollment["student_id"] == enrollment_data.student_id:
            student_exists = True
        if enrollment["course_id"] == enrollment_data.course_id:
            course_exists = True
    if not student_exists:
        raise HTTPException(status_code=400, detail="Student does not exist")
    if not course_exists:
        raise HTTPException(status_code=400, detail="Course does not exist")

    new_enrollment = {
        "id": enrollment_id,
        "student_id": enrollment_data.student_id,
        "course_id": enrollment_data.course_id,
    }

    enrollments.append(new_enrollment)

    return {
        "status": "success",
        "new_enrollment": new_enrollment
    }

@router.delete("/enrollments/deregister/{enrollment_id}")
def deregister_student(enrollment_id: int, student_data: StudentCheck = Depends()):
    if student_data.role != "student":
        raise HTTPException(status_code=401, detail="You are not a student! Get out!")
    
    enrollment_exists = False

    for enrollment in enrollments:
        if enrollment["id"] == enrollment_id:
            enrollment_exists = True
            enrollments.remove(enrollment)
            return {
                "status": "success",
                "message": "enrollment removed"
            }
    if not enrollment_exists:
        raise HTTPException(status_code=404, detail="Enrollment does not exist.")
    
@router.get("/admin/enrollments")
def get_all_enrollment(admin_data: AdminCheck = Depends()):
    if admin_data.role != "admin":
        raise HTTPException(status_code=401, detail="You are not an admin! Get out!") 
    return enrollments
    

@router.get("/admin/enrollment/{course_id}")
def get_enrollment(course_id: int, admin_data: AdminCheck = Depends()):
    if admin_data.role != "admin":
        raise HTTPException(status_code=401, detail="You are not an admin! Get out!") 
    for enrollment in enrollments:
        if enrollment["course_id"] == course_id:
            return enrollment
    raise HTTPException(status_code=404, detail="Enrollment not found.")


@router.delete("/admin/force-deregister/{enrollment_id}")
def deregister_student(enrollment_id: int, admin_data:  AdminCheck = Depends ()):
    if admin_data.role != "admin":
        raise HTTPException(status_code=401, detail="You are not an admin! Get out!") 
    
    enrollment_exists = False

    for enrollment in enrollments:
        if enrollment["id"] == enrollment_id:
            enrollment_exists = True
            enrollments.remove(enrollment)
            return {
                "status": "success",
                "message": "enrollment removed"
            }
    if not enrollment_exists:
        raise HTTPException(status_code=404, detail="Enrollment does not exist.")