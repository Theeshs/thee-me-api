from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.handlers.users.types import Credentials, User, UserSkillAssignment
from thee_me.services.user_service import (
    create_user,
    list_users,
    login_user,
    thee_me,
    user_skill_add,
)
from typing import  List

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: User, db: Session = Depends(get_async_db)):
    try:
        user.email = validate_email(user.email).normalized
        user = await create_user(db, user)
        return user
    except EmailNotValidError:
        return JSONResponse(
            {"error": "Invalid email"}, status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/login")
async def login(
    creds: Credentials,
    db: Session = Depends(get_async_db),
    Authorize: AuthJWT = Depends(),
):
    return await login_user(db, creds, Authorize)


@router.get("/users")
async def users(db: Session = Depends(get_async_db)):
    return await list_users(db)


@router.get("/me")
async def me(db: Session = Depends(get_async_db)):
    return await thee_me(db)


@router.put("/user/{user_id}/skills")
async def user_skill(
    user_id: int, skill_data: UserSkillAssignment, db: Session = Depends(get_async_db)
):
    return await user_skill_add(db, user_id, skill_data.skills)
