from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    project_link: Optional[str] = None
    technologies: Optional[str] = None

    class Config:
        orm_mode = True
