from __future__ import annotations

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session, aliased, selectinload

from thee_me.education.handler import list_educations
from thee_me.user_services.handler import get_user_services
from thee_me.user_services.types import UserServiceType as UserServiceTypeSerializer

from ..education.types import EducationReturn as EducationSerializer
from ..experience.types import Experience as ExperianceSerializer
from ..models.user import (
    Educations,
    Experience,
    Repositories,
    Skill,
    User,
    UserSkillAssociation,
)
from ..skills.types import Skill as SkillSerializer
from .types import ResponseUser
from .types import User as UserType


async def get_user_repositories(db: Session, user: str, limit: int = None, tech: str = None):
    query = (
        select(Repositories)
        .where(Repositories.user == user)
        .order_by(desc(Repositories.repo_created_at))
    )

    if tech:
        query = query.where(Repositories.repo_language == tech)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query.distinct())
    repositories = result.scalars().all()
    return repositories


async def save_user(db: Session, user: UserType):
    try:
        user_ = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "dob": user.dob,
            "description": user.description,
            "email": user.email,
            "github_username": user.github_username,
            "username": user.username,
            "mobile_number": 81502210,
        }
        db_user = User(**user_)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return user
    except Exception as e:
        print(e)


async def get_user(db: Session, email: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        # Assuming User is a SQLAlchemy model
        return user
    return None


async def get_user_by_user_id(db: Session, user_id: int, raw_object=False):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if raw_object:
        return user
    if user:
        # Assuming User is a SQLAlchemy model
        user_obj = UserType.from_orm(user)
        return user_obj
    return None


async def list_all_users(db: Session):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def list_user_skills(db: Session, user_id: int):
    stmt = (
        select(Skill, UserSkillAssociation.percentage)
        .select_from(Skill)
        .join(UserSkillAssociation)
        .options(selectinload(Skill.user_association))
        .where(UserSkillAssociation.user_id == user_id)
    )
    result = await db.execute(stmt)
    if result:
        result = result.scalars().all()
    # skills = [for ]
    skills = [
        {"name": skill_obj.name, "percentage": skill_obj.user_association[0].percentage}
        for skill_obj in result
    ]
    return skills


async def me(db: Session):
    user = await get_user(db, "theekshana.sandaru@gmail.com")
    educations = await list_educations(db, user.id)
    experiences = await db.execute(
        select(Experience)
        .where(Experience.user_id == user.id)
        .order_by(desc(Experience.start_date))
    )
    experiences = experiences.scalars().all()
    skills = await list_user_skills(db, user.id)
    user_services_ = await get_user_services(db, user)
    repositories = await get_user_repositories(db, user, 5, None)

    me_user = ResponseUser(
        first_name=user.first_name,
        last_name=user.last_name,
        dob=user.dob,
        username=user.username,
        email=user.email,
        github_username=user.github_username,
        description=user.description,
        recidential_country=user.recidential_country,
        address_block=user.address_block,
        address_street=user.address_street,
        mobile_number=user.mobile_number,
        nationality=user.nationality,
        skills=[SkillSerializer.parse_obj(item) for item in skills if item],
        experience=[ExperianceSerializer.from_orm(exp) for exp in experiences if exp],
        education=[EducationSerializer.from_orm(edu) for edu in educations if edu],
        user_services=[service for service in user_services_ if service],
        repositories=[repo for repo in repositories if repo],
    )

    return me_user


async def assign_skill_to_user(db: Session, skill_list: list, user_id: int):
    for skill in skill_list:
        actual_skill = await db.execute(select(Skill).where(Skill.name == skill.name))
        result = actual_skill.scalar_one_or_none()
        new_record = UserSkillAssociation(
            user_id=user_id, skill_id=result.id, percentage=skill.percentage
        )
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record
