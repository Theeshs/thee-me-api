from sqlalchemy import create_engine, engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:mysecretpassword@127.0.0.1:5432/theesh.me"
)

SQLALCHEMY_DATABASE_URL_ASYNC = (
    "postgresql+asyncpg://postgres:mysecretpassword@127.0.0.1:5432/theesh.me"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def get_async_db():
    try:
        async with async_session() as db:
            yield db
    except Exception as e:
        print(e)
