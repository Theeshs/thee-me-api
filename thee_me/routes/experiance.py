"""experience apis"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.handlers.experiences.types import Experience
from thee_me.middlewares.auth_middleware import get_current_user
from thee_me.services.experience_service import create_user_experience, list_experiences

router = APIRouter()


@router.post("/experiences")
async def experiences(
    experience: Experience,
    db: Session = Depends(get_async_db),
    current_user: dict = Depends(get_current_user),
):
    """creating user experiences"""
    return await create_user_experience(db, current_user.get("email"), experience)


@router.get("/experiences")
async def list_user_experiences(
    db: Session = Depends(get_async_db),
    current_user: dict = Depends(get_current_user),
):
    """listing user experiences"""
    return await list_experiences(db, current_user["id"])
