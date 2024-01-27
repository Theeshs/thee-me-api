from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db, get_db

from ..skills.controller import (
    _get_skill_by_name,
    create_skill_v2,
    get_all_skills,
    remove_skill,
    skill_create,
)
from .types import SkillCreate, SkillV2

skills_router = APIRouter()


@skills_router.get("/skills")
async def list_skills(db: Session = Depends(get_async_db)):
    return await get_all_skills(db)


@skills_router.post("/skills")
async def create_user_skill(skill: SkillCreate, db: Session = Depends(get_async_db)):
    return await skill_create(db, skill)


@skills_router.get("/skills/{skil_name}")
async def get_skill_by_name(skill_name, db: Session = Depends(get_async_db)):
    return await _get_skill_by_name(db, skill_name)


@skills_router.delete("/skills/{skill_name}")
async def delete_skill(skill_name: str, db: Session = Depends(get_async_db)):
    return await remove_skill(db, skill_name)


@skills_router.get("/v2/skills")
async def skills_list(db: Session = Depends(get_async_db)):
    return await get_all_skills(db)


@skills_router.post("/v2/skills")
async def skills_create_v2(skill: SkillV2, db: Session = Depends(get_async_db)):
    return await create_skill_v2(skill, db)
