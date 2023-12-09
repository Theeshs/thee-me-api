from sqlalchemy.orm import Session
from thee_me.models.user import User, UserService
from sqlalchemy import select
async def get_user_services(db: Session, user: User = None):
    if not user:
        pass

    result = await db.execute(
        select(UserService).where(UserService.user == user)
    )

    services = result.scaler().all()
    return services

