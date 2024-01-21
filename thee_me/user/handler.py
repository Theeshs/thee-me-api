from sqlalchemy import select
from sqlalchemy.orm import Session, aliased, selectinload

from ..education.types import EducationReturn as EducationSerializer
from ..experience.types import Experience as ExperianceSerializer
from ..models.user import Skill, User, UserSkillAssociation
from ..skills.types import Skill as SkillSerializer
from .types import ResponseUser
from .types import User as UserType


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
    print("me")
    stmt = (
        select(User, Skill)
        .select_from(User)
        .options(selectinload(User.experience))
        .options(selectinload(User.education))
        .where(User.email == "theekshana.sandaru@gmail.com")
        .limit(1)
    )

    result = await db.execute(stmt)
    if result:
        result = result.scalar_one_or_none()
        skills = await list_user_skills(db, result.id)
        me_user = ResponseUser(
            first_name=result.first_name,
            last_name=result.last_name,
            dob=result.dob,
            username=result.username,
            email=result.email,
            github_username=result.github_username,
            description=result.description,
            recidential_country=result.recidential_country,
            address_block=result.address_block,
            address_street=result.address_street,
            mobile_number=result.mobile_number,
            nationality=result.nationality,
            skills=[SkillSerializer.parse_obj(item) for item in skills if item],
            experience=[
                ExperianceSerializer.from_orm(exp) for exp in result.experience if exp
            ],
            education=[
                EducationSerializer.from_orm(edu) for edu in result.education if edu
            ],
        )
        return me_user
    return None


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
    # result = await db.execute(select(Skill).where(Skill.name.in_(skill_list)))
    # skill = result.scalar_one_or_none()
    # skills = [skill.id for skill in result.scalars().all() if skill]
    # new_skill_records = []
    # for skill in skills:
    #     new_skill_records.append({"skill_id": skill, "user_id": user_id})
    # delete_statement = delete(UserSkillAssociation).where(
    #     UserSkillAssociation.user_id == user_id
    # )
    # result = await db.execute(delete_statement)
    # deleted_rows = result.rowcount
    # await db.commit()
    # print(deleted_rows)
    # await db.execute(UserSkillAssociation.__table__.insert().values(new_skill_records))
    # await db.commit()
