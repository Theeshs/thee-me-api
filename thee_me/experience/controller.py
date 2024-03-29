from sqlalchemy.orm import Session

from .handler import create_experience, get_experiences
from .types import Experience


async def user_experiences_list_service(db: Session, user_id: int):
    """list all the user experiences
    :db - database connnetion
    :user_id - id of the logged user
    """
    experiences = await get_experiences(db, user_id)
    if not experiences:
        raise Exception("No experiences found")


async def create_user_experience(db: Session, user_email: str, experience: Experience):
    """creating the user experience"""
    return await create_experience(db, user_email, experience)


async def list_experiences(db: Session, user: int):
    """helper function for user experience list"""
    return await get_experiences(db, user)
