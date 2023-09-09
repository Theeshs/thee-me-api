from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from thee_me.handlers.educations.types import EducationCreate, EducationReturn
from thee_me.models.user import Educations


async def list_educations(db: Session, user_id: int):
    result = await db.execute(select(Educations).where(Educations.user_id == user_id))
    educations = result.scalars().all()
    return educations


async def create_education(db: Session, user_id: int, payload: EducationCreate):
    education = payload.dict()
    education["user_id"] = user_id
    db_education = Educations(**education)
    db.add(db_education)
    await db.commit()
    await db.refresh(db_education)
    return db_education
