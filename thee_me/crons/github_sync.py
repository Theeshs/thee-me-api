import requests
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from fastapi import Depends
from thee_me.database.connection import get_async_db, get_db
from thee_me.models.user import Repositories, User
from datetime import datetime


async def sync_github_repositories(username: str, db: Session) -> None:
    user = await db.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()

    user_repositories =  await db.execute(
        select(Repositories).where(Repositories.user_id == user.id)
    )
    url = f"https://api.github.com/users/{user.github_username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        for repo in response.json():
            print(repo)
            new_repo = Repositories(
                repo_name=repo.get("name", "No Name"),
                repo_description=repo.get("description"),
                user_id=user.id,
                repo_url=repo.get("html_url"),
                repo_language=repo.get("language"),
                repo_created_at=datetime.strptime(repo.get("created_at"), '%Y-%m-%dT%H:%M:%SZ'),
                repo_updated_at=datetime.strptime(repo.get("updated_at"), '%Y-%m-%dT%H:%M:%SZ'),
                show_on_profile=False,
                order=0,
            )
            db.add(new_repo)
            await db.commit()
            await db.refresh(new_repo)

    else:
        print("not found")
