from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.contact_me.contorller import send_and_store_email
from thee_me.contact_me.types import MessageRequest
from thee_me.database.connection import get_async_db

contact_router = APIRouter()


@contact_router.post("/contact-me")
async def contact_me(message: MessageRequest, db: Session = Depends(get_async_db)):
    """Contact me service"""
    success = await send_and_store_email(db, message)
    if not success:
        return {"status": "failed", "message": "Error sending email"}
    return {"status": "success", "message": "Email sent!"}
