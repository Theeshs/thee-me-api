import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from thee_me.contact_me.handler import send_email
from thee_me.contact_me.types import MessageRequest

load_dotenv()


async def send_and_store_email(db: Session, msg_data: MessageRequest):
    try:
        to_email = os.getenv("THEE_CONTACT_EMAIL")
        from_email = os.getenv("EMAIL_SENDER_ADDRESS")
        password = os.getenv("EMAIL_ACCESS_KEY")
        return await send_email(
            from_email, to_email, msg_data.subject, msg_data.message, password
        )
    except Exception as e:
        return False
