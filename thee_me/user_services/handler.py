from sqlalchemy import select
from sqlalchemy.orm import Session

from thee_me.models.user import User, UserService

from .types import UserServiceType


async def get_user_services(db: Session, user: User = None):
    if not user:
        pass

    result = await db.execute(select(UserService).where(UserService.user == user))

    services = result.scalars().all()
    return services


async def create_user_services(db: Session, user: User, service_dict: UserServiceType):
    if not user:
        raise Exception("User not available")
    service_dict = service_dict.dict()
    service_dict["user_id"] = user.id
    new_service = UserService(**service_dict)

    db.add(new_service)

    await db.commit()
    await db.refresh(new_service)
    return new_service
