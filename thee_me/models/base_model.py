from sqlalchemy import Column, DateTime, Integer, func

from thee_me.database.connection import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
