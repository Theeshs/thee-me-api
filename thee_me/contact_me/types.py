from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    message: str
    call_back_email: str
    name: str
    subject: str

    class Config:
        orm_mode = True
