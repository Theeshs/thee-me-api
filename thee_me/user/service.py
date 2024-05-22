from typing import List

from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from thee_me.crons.github_sync import sync_github_repositories
from thee_me.database.connection import get_async_db

from .controller import (
    create_user,
    list_users,
    login_user,
    thee_me,
    user_repos,
    user_skill_add,
)
from .types import Credentials, User, UserSkillAssignment

user_router = APIRouter()


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: User, db: Session = Depends(get_async_db)):
    try:
        user.email = validate_email(user.email).normalized
        user = await create_user(db, user)
        return user
    except EmailNotValidError:
        return JSONResponse(
            {"error": "Invalid email"}, status_code=status.HTTP_400_BAD_REQUEST
        )


@user_router.post("/login")
async def login(
    creds: Credentials,
    db: Session = Depends(get_async_db),
    Authorize: AuthJWT = Depends(),
):
    return await login_user(db, creds, Authorize)


@user_router.get("/users")
async def users(db: Session = Depends(get_async_db)):
    return await list_users(db)


@user_router.get("/me")
async def me(db: Session = Depends(get_async_db)):
    return await thee_me(db)


@user_router.put("/user/{user_id}/skills")
async def user_skill(
    user_id: int, skill_data: UserSkillAssignment, db: Session = Depends(get_async_db)
):
    return await user_skill_add(db, user_id, skill_data.skills)


@user_router.get("/user/sync_repositories")
async def git_sync(db: Session = Depends(get_async_db)):
    await sync_github_repositories("thee", db)
    return {"status": "success"}


@user_router.get("/user/git_repositories")
async def git_repositories(db: Session = Depends(get_async_db), limit: int = None, tech: str = None):
    repos = await user_repos("theekshana.sandaru@gmail.com", db, limit, tech)
    return repos
