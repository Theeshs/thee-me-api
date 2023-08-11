from datetime import date

from pydantic import BaseModel, Field
from typing import Optional, List


class Skill(BaseModel):
    name: str
    percentage: int

    class Config:
        orm_mode = True


class SkillCreate(BaseModel):
    name: str = Field(..., description="name of the skill")
    percentage: int = Field(..., description="skill percentage")

    class Config:
        orm_mode = True


class SkillWithName(BaseModel):
    name: Optional[List[str]]

    class Config:
        orm_mode = True
