from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.middlewares.auth_middleware import get_current_user
from thee_me.models.user import UserService

from .controller import create_user_service, get_user_services
from .types import UserServiceType

service_router = APIRouter()


@service_router.get("/services")
async def get_service(
    db: Session = Depends(get_async_db), current_user: dict = Depends(get_current_user)
):
    services = await get_user_services(current_user.get("email"), db)

    return services


@service_router.post("/services")
async def add_user_service(
    service: UserServiceType = None,
    db: Session = Depends(get_async_db),
    current_user: dict = Depends(get_current_user)
):
    service = await create_user_service(current_user.get("email"), service, db)
    return service
