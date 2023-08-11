from ..handlers.experiences.types import Experience
from ..handlers.experiences.experience_handler import get_experiences, create_experience
from sqlalchemy.orm import Session


async def user_experiences_list_service(db: Session, user_id: int):
    experiences = await get_experiences(db, user_id)
    if not experiences:
        raise Exception("No experiences found")


async def create_user_experience(db: Session, user_email: str, experience: Experience):
    return await create_experience(db, user_email, experience)
