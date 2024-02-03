from sqlalchemy.orm import Session
from thee_me.projects.types import Project
from thee_me.user.handler import get_user
from .hander import list_prjects


async def list_projects(email: str, db: Session):
    user = await get_user(email=email, db=db)
    if not user:
        raise Exception("User not found")

    return


def create_project(user: str, db: Session, project: Project):
    return None