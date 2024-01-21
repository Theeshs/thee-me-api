from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..models.user import Skill
from .types import Skill as SkillResponse
from .types import SkillCreate


async def list_all_skills(db: Session):
    result = await db.execute(select(Skill))
    skills = result.scalars().all()
    return skills


async def get_skill(db: Session, skill_name: str):
    result = await db.execute(select(Skill).where(Skill.name == skill_name))
    skill = result.scalar_one_or_none()
    if skill:
        # Assuming User is a SQLAlchemy model
        skill_obj = SkillResponse.from_orm(skill)
        return skill_obj
    return None


async def create_skill(db: Session, skill: SkillCreate):
    create_request = {"name": skill.name, "percentage": skill.percentage}
    db_skill = Skill(**create_request)
    db.add(db_skill)
    await db.commit()
    await db.refresh(db_skill)
    return skill


async def delete_skill(db: Session, skill_name: str):
    statment = delete(Skill).where(Skill.name == skill_name)
    result = await db.execute(statment)
    deleted_rows = result.rowcount
    await db.commit()
    if deleted_rows:
        return True
    else:
        raise Exception("Unable to delete the skill")


async def save_skill(skill_name: str, db: Session):
    skill = Skill(name=skill_name)
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill
