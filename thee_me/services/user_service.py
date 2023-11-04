import json

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from ..handlers.users.types import Credentials, ResponseUser, User
from ..handlers.users.user_handler import (
    assign_skill_to_user,
    get_user,
    get_user_by_user_id,
    list_all_users,
    me,
    save_user,
)
from ..utils.password_utils import match_password, set_password_hash


async def create_user(db: Session, user: User):
    if await get_user(db, user.email):
        raise Exception("User already exists")

    user.password = set_password_hash(user.password)

    user = await save_user(db, user)

    return user


async def login_user(db: Session, creds: Credentials, Authorize: AuthJWT):
    user: User = await get_user(db, creds.email)
    if not user:
        raise Exception("Unauthorized")
    if not await match_password(creds.password, user.password):
        raise Exception("Unauthorized")
    return {
        "access_token": Authorize.create_access_token(
            subject=json.dumps(
                {
                    "username": user.username,
                    "email": user.email,
                    "id": user.id if user.id else None,
                }
            )
        ),
        "refresh_token": Authorize.create_refresh_token(
            subject=json.dumps(
                {
                    "username": user.username,
                    "email": user.email,
                    "id": user.id if user.id else None,
                }
            )
        ),
    }


async def list_users(db: Session):
    users = await list_all_users(db)
    users = [ResponseUser.from_orm(user).dict() for user in users]
    return users


async def thee_me(db: Session):
    iam = await me(db)
    return iam.dict()


async def user_skill_add(db: Session, user_id: int, skill_list: list):
    user = await get_user_by_user_id(db, user_id, raw_object=True)
    if not user:
        raise Exception("No user available")
    await assign_skill_to_user(db, skill_list, user_id)
