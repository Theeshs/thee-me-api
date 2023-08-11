from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db, get_db
from ..services.experience_service import create_user_experience
from ..handlers.experiences.types import Experience
from ..middlewares.auth_middleware import get_current_user

router = APIRouter()


@router.post("/experiences")
async def experiences(experience: Experience, db: Session = Depends(get_async_db), current_user: dict = Depends(get_current_user), ):
    return await create_user_experience(db, current_user.get("email"), experience)
