import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load .env file
load_dotenv()

# Now you can access the variables
database_url = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:"
    f"{os.environ.get('DB_PORT')}/{os.environ.get('DATABASE')}"
)

SQLALCHEMY_DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:"
    f"{os.environ.get('DB_PORT')}/{os.environ.get('DATABASE')}"
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
            print("Connected to database")
            yield db
    except Exception as e:
        print(e)
