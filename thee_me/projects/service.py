from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from thee_me.database.connection import get_async_db
from thee_me.middlewares.auth_middleware import get_current_user
from .controller import save_project, list_all_projects
from thee_me.projects.types import Project

project_router = APIRouter()


@project_router.get("/project-list")
async def list_projects(db: Session = Depends(get_async_db), current_user: dict = Depends(get_current_user)):
    return await list_all_projects(current_user.get("email"), db)


@project_router.post("/project-create")
async def create_project(
    db: Session = Depends(get_async_db),
    project: Project = None,
    current_user: dict = Depends(get_current_user),
):
    return await save_project(current_user.get("email"), db, project)
