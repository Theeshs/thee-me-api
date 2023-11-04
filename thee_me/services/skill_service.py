from sqlalchemy.orm import Session
from typing import Dict
from ..handlers.skills.skills_handler import save_skill
from ..handlers.skills.types import SkillV2

from thee_me.handlers.skills.skills_handler import (
    create_skill,
    delete_skill,
    get_skill,
    list_all_skills,
)
from thee_me.handlers.skills.types import Skill, SkillCreate


async def get_all_skills(db: Session):
    skills = await list_all_skills(db)
    formatted_skills = [SkillV2.from_orm(skill).dict().get("name ") for skill in skills]
    return formatted_skills


async def skill_create(db: Session, skill: SkillCreate):
    skill_found: Skill = await get_skill(db, skill.name)
    if skill_found:
        raise Exception("Skill already available")
    return await create_skill(db, skill)


async def _get_skill_by_name(db: Session, skill_name: str):
    skill_found: Skill = await get_skill(db, skill_name)
    return skill_found


async def remove_skill(db: Session, skill_name: str):
    skill_found: Skill = await get_skill(db, skill_name)
    if not skill_found:
        raise Exception("No skill found")
    await delete_skill(db, skill_found.name)
    return True


async def get_all_skills_v2(db: Session):
    return


async def create_skill_v2(request_data: SkillV2, db: Session):
    return await save_skill(request_data.name, db)
