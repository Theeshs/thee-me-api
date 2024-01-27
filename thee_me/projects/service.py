from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.middlewares.auth_middleware import get_current_user
from thee_me.projects.types import Project

project_router = APIRouter()


@project_router.get("/project-list")
def list_projects(db: Session = Depends(get_async_db)):
    return NotImplemented("Not Implemented")


@project_router.post("/project-create")
def create_project(
    db: Session = Depends(get_async_db),
    project: Project = None,
    current_user: dict = Depends(get_current_user),
):
    return NotImplemented("Not Implemented")
