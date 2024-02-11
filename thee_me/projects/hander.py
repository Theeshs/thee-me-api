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
    new_project = UserProject(
        name=project_data.name,
        description=project_data.description,
        from_date=project_data.from_date,
        to_date=project_data.to_date,
        project_link=project_data.project_link,
        technologies=project_data.technologies,
        user_id=user_id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project