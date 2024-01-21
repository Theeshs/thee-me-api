"""education api routes"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.middlewares.auth_middleware import get_current_user

from .controller import get_all_educations, save_education
from .types import EducationCreate, EducationReturn

education_router = APIRouter()


@education_router.get("/education")
async def list_educations(
    db: Session = Depends(get_async_db), current_user: dict = Depends(get_current_user)
) -> List[EducationReturn]:
    """API endpoint for user education list"""
    return await get_all_educations(db, current_user["id"])


@education_router.post("/education")
async def create_education(
    payload: EducationCreate,
    db: Session = Depends(get_async_db),
    current_user: dict = Depends(get_current_user),
):
    return await save_education(db, current_user["id"], payload)
