from sqlalchemy.orm import Session
from ..models.user import UserProject
from .types import Project
from typing import List
from sqlalchemy import select
async def list_projects(db: Session, user_id: int) -> List[Project]:
    result = await db.execute(select(UserProject).where(UserProject.user_id == user_id))
    projects = result.scalars().all()
    return projects