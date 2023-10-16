from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    dob = Column(DateTime, nullable=True)
    username = Column(String(150), nullable=False)
    password = Column(String(350), nullable=False)
    email = Column(String(150), nullable=False)
    github_username = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    mobile_number = Column(Integer, default=81502210)
    address_block = Column(String(50), nullable=True, default="#04-181")
    address_street = Column(String(250), nullable=True,
                            default="311, Hougang Avenue 5")
    recidential_country = Column(
        String(60), nullable=True, default="Singapore")
    nationality = Column(String(70), default="Sri Lankan")
    skills = relationship(
        "Skill",
        secondary="user_skill_association",
        back_populates="users",
        lazy="selectin",
    )
    experience = relationship("Experience", back_populates="user")
    education = relationship("Educations", back_populates="user")
    mobile_number = Column(Integer, nullable=False)


class Skill(BaseModel):
    __tablename__ = "skill"

    name = Column(String(150), nullable=False)
    users = relationship(
        "User",
        secondary="user_skill_association",
        back_populates="skills",
        lazy="selectin",
    )


class UserSkillAssociation(BaseModel):
    __tablename__ = "user_skill_association"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    )
    skill_id = Column(
        Integer,
        ForeignKey("skill.id", ondelete="CASCADE"),
        nullable=True,
    )
    percentage = Column(Integer, nullable=True)


class Experience(BaseModel):
    __tablename__ = "experience"

    company_name = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    current_place = Column(Boolean, nullable=True)
    position = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="experience")


class Educations(BaseModel):
    __tablename__ = "education"
    institue_name = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    mode_of_study = Column(String(200), nullable=False)
    degree_type = Column(String(200), nullable=False)
    area_of_study = Column(String(200), nullable=False)
    currenty_studying = Column(Boolean, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="education")
