from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db, get_db

from ..handlers.skills.types import SkillCreate
from ..services.skill_service import (
    _get_skill_by_name,
    get_all_skills,
    remove_skill,
    skill_create,
)

router = APIRouter()


@router.get("/skills")
async def list_skills(db: Session = Depends(get_async_db)):
    return await get_all_skills(db)


@router.post("/skills")
async def create_user_skill(skill: SkillCreate, db: Session = Depends(get_async_db)):
    return await skill_create(db, skill)


@router.get("/skills/{skil_name}")
async def get_skill_by_name(skill_name, db: Session = Depends(get_async_db)):
    return await _get_skill_by_name(db, skill_name)


@router.delete("/skills/{skill_name}")
async def delete_skill(skill_name: str, db: Session = Depends(get_async_db)):
    return await remove_skill(db, skill_name)


@router.get("/v2/skills")
async def skills_list(db: Session = Depends(get_async_db)):
    return await get_all_skills(db)
