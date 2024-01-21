from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class EducationCreate(BaseModel):
    institue_name: str
    start_date: date
    end_date: date = None
    currenty_studying: bool
    degree_type: str
    area_of_study: str
    mode_of_study: str

    class Config:
        orm_mode = True


class EducationReturn(BaseModel):
    id: int
    institue_name: str
    start_date: date
    end_date: date = None
    currenty_studying: bool
    degree_type: str
    area_of_study: str
    mode_of_study: str

    class Config:
        orm_mode = True
