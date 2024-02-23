from sqlalchemy.orm import Session

from thee_me.models.user import UserService

from ..user.handler import get_user
from .handler import create_user_services as create_user_service_handler
from .handler import get_user_services as get_user_services_handler
from .types import UserServiceType


async def get_user_services(email: str = None, db: Session = None):
    user = await get_user(db, email)

    if not user:
        raise Exception("User not available")
    services = await get_user_services_handler(db, user)
    return services


async def create_user_service(email: str, service: UserServiceType, db: Session):
    user = await get_user(db, email)
    if not user:
        raise Exception("User not found")

    service = await create_user_service_handler(db, user, service)
    return service


def update_user_service(email: str, service_id: int, db: Session):
    pass
