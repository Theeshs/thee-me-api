from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from ...models.user import Experience
from ...handlers.experiences.types import Experience as ExperienceRequest
from ...handlers.users.user_handler import get_user


async def get_experiences(db: Session, user_id: int):
    result = db.execute(select(Experience).where(
        Experience.user_id == user_id))
    experiences = result.scalars().all()
    return experiences


async def get_experience(db: Session, id: int, user_id: int):
    result = await db.execute(select(Experience).where(Experience.id == id, Experience.user_id == user_id))
    experience = result.scalar_one_or_none()
    return experience


async def create_experience(db: Session, user_email: str, experience: ExperienceRequest):
    user = await get_user(db, user_email)
    experience = experience.dict()
    experience["user_id"] = user.id
    db_experience = Experience(**experience)
    db.add(db_experience)
    await db.commit()
    await db.refresh(db_experience)
    return db_experience
