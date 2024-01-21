""" service controllers for the educations """
from sqlalchemy.orm import Session

from .handler import create_education, list_educations
from .types import EducationCreate


async def get_all_educations(db: Session, user_id: int):
    """get all user educations"""
    return await list_educations(db, user_id)


async def save_education(db: Session, user_id: int, payload: EducationCreate):
    return await create_education(db, user_id, payload)
