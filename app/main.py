from fastapi import FastAPI

from app.routes.user_route import router as user_router
from app.routes.course_route import router as course_router
from app.routes.enrollment_route import router as enrollment_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Course Enrollment Management")

app.include_router(user_router)
app.include_router(course_router)
app.include_router(enrollment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)