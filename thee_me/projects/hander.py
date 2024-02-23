from sqlalchemy.orm import Session
from ..models.user import UserProject
from .types import Project
from typing import List
from sqlalchemy import select
async def get_projects(db: Session, user_id: int) -> List[Project]:
    result = await db.execute(select(UserProject).where(UserProject.user_id == user_id))
    projects = result.scalars().all()
    return projects

async def create_project(db: Session, project_data: Project, user_id: int):
    project = project_data.dict()
    name = project.pop("name")
    project["project_name"] = name
    project["user_id"] = user_id
    new_project = UserProject(**project)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project