from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class UserServiceType(BaseModel):
    service_name = str
    service_description = str
    service_icon = str

    class Config:
        orm_mode = True
