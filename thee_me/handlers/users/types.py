from datetime import date

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from typing import List
from ..skills.types import Skill
from ..experiences.types import Experience


class User(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    username: str = Field(..., description="username of the user")
    password: str = Field(..., description="password of the user")
    email: EmailStr
    github_username: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[Skill]] = []

    class Config:
        orm_mode = True


class Credentials(BaseModel):
    email: str = Field(..., description="email of the user")
    password: str = Field(..., description="password of the user")


class ResponseUser(BaseModel):
    first_name: str
    last_name: str
    dob: date
    username: str = Field(..., description="username of the user")
    email: str = Field(..., description="email of the user")
    github_username: str
    description: str
    skills: Optional[List[Skill]] = []
    experience: Optional[List[Experience]]

    class Config:
        orm_mode = True


class UserSkillAssignment(BaseModel):
    skills: List[str]
