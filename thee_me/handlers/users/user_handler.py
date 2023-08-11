from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ...models.user import User, Skill, UserSkillAssociation, Experience
from .types import User as UserType, ResponseUser
from ..skills.types import Skill as SkillSerializer


async def save_user(db: Session, user: UserType):
    user_ = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "dob": user.dob,
        "description": user.description,
        "email": user.email,
        "github_username": user.github_username,
        "username": user.username,
    }
    db_user = User(**user_)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return user


async def get_user(db: Session, email: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        # Assuming User is a SQLAlchemy model
        user_obj = UserType.from_orm(user)
        return user_obj
    return None


async def get_user_by_user_id(db: Session, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        # Assuming User is a SQLAlchemy model
        user_obj = UserType.from_orm(user)
        return user_obj
    return None


async def list_all_users(db: Session):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def me(db: Session):
    stmt = (
        select(User, Skill)
        .select_from(User)
        .outerjoin(UserSkillAssociation)
        .outerjoin(Skill)
        .options(selectinload(User.skills))
        .where(User.email == "theekshana.sandaru@gmail.com")
    )
    result = await db.execute(stmt)
    if result:
        result = result.scalar_one_or_none()
        me = ResponseUser(
            first_name=result.first_name,
            last_name=result.last_name,
            dob=result.dob,
            username=result.username,
            email=result.email,
            github_username=result.github_username,
            description=result.description,
            skills=[
                SkillSerializer.from_orm(item) for item in result.skills if item],
        )
        return me
    return None


async def assign_skill_to_user(db: Session, skill_list: list, user_id: int):
    result = await db.execute(select(Skill).where(Skill.name.in_(skill_list)))
    skills = [skill.id for skill in result.scalars().all() if skill]
    new_skill_records = []
    for skill in skills:
        new_skill_records.append({
            "skill_id": skill,
            "user_id": user_id
        })
    await db.execute(UserSkillAssociation.__table__.insert().values(new_skill_records))
    await db.commit()
