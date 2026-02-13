from fastapi import APIRouter, Depends, HTTPException
from app.schemas.users_schema import UserCreate
from app.models.users import users

router = APIRouter()

@router.post("/users")
def create_user(user_data: UserCreate):
    current_user_id = users[-1]["id"] + 1

    new_user = {
        "id": current_user_id,
        "name": user_data.name,
        "email": user_data.email,
        "role" : user_data.role,
    }

    users.append(new_user)

    return {
        "status": "success",
        "new_user": new_user
    }

@router.get("/users")
def get_all_user():
    return users


@router.get("/users/{id}")
def get_user(id: int):
    for user in users:
        if user["id"] == id:
            return user
        return {"error": "User not found"}
