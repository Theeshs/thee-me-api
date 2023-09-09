from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from ...models.user import Experience, Skill, User, UserSkillAssociation, Educations
from thee_me.handlers.experiences.types import Experience as ExperianceSerializer
from thee_me.handlers.skills.types import Skill as SkillSerializer
from thee_me.handlers.educations.types import EducationReturn as EducationSerializer
from .types import ResponseUser
from .types import User as UserType


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
        .outerjoin(Experience)
        .outerjoin(Educations)
        .options(selectinload(User.skills))
        .options(selectinload(User.experience))
        .options(selectinload(User.education))
        .where(User.email == "theekshana.sandaru@gmail.com")
        .limit(1)
    )
    result = await db.execute(stmt)
    if result:
        result = result.scalar_one_or_none()
        me_user = ResponseUser(
            first_name=result.first_name,
            last_name=result.last_name,
            dob=result.dob,
            username=result.username,
            email=result.email,
            github_username=result.github_username,
            description=result.description,
            skills=[SkillSerializer.from_orm(item) for item in result.skills if item],
            experience=[
                ExperianceSerializer.from_orm(exp) for exp in result.experience if exp
            ],
            education=[
                EducationSerializer.from_orm(edu) for edu in result.education if edu
            ]
        )
        return me_user
    return None


async def assign_skill_to_user(db: Session, skill_list: list, user_id: int):
    result = await db.execute(select(Skill).where(Skill.name.in_(skill_list)))
    skills = [skill.id for skill in result.scalars().all() if skill]
    new_skill_records = []
    for skill in skills:
        new_skill_records.append({"skill_id": skill, "user_id": user_id})
    delete_statement = delete(UserSkillAssociation).where(
        UserSkillAssociation.user_id == user_id
    )
    result = await db.execute(delete_statement)
    deleted_rows = result.rowcount
    await db.commit()
    print(deleted_rows)
    await db.execute(UserSkillAssociation.__table__.insert().values(new_skill_records))
    await db.commit()
