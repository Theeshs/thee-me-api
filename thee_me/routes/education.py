from fastapi import APIRouter, Depends
from thee_me.middlewares.auth_middleware import get_current_user
from thee_me.database.connection import get_async_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/education")
def list_educations(db: Session = Depends(get_async_db), current_user: dict = Depends(get_current_user)) -> List[dict]:
    return []
