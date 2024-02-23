from sqlalchemy.orm import Session
from thee_me.projects.types import Project
from thee_me.user.handler import get_user
from .hander import get_projects, create_project


async def list_all_projects(email: str, db: Session):
    user = await get_user(email=email, db=db)
    if not user:
        raise Exception("User not found")

    return await get_projects(db=db, user_id=user.id)


async def save_project(user: str, db: Session, project: Project):
    user = await get_user(db, user)

    if not user:
        raise Exception("User not found")

    return await create_project(db, project, user.id)
