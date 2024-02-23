from typing import Optional

from pydantic import BaseModel


class UserServiceType(BaseModel):
    service_name = str
    service_description = str
    service_icon = str

    class Config:
        orm_mode = True


class UserServiceReq(BaseModel):
    service_name: str
    service_description: Optional[str]
    service_icon: Optional[str]

    class Config:
        orm_mode = True
