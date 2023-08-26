from datetime import date

from pydantic import BaseModel, Field
from typing import Optional, List


class Experience(BaseModel):
    company_name: str
    start_date: date
    end_date: date = None
    current_place: bool
    position: str

    class Config:
        orm_mode = True
