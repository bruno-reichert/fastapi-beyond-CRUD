from sqlmodel import SQLModel, create_engine, Session, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.db.models import Book

async_engine = create_async_engine(url = Config.DATABASE_URL)

async def init_db():
    async with async_engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession: # type: ignore
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False # type: ignore
    ) # type: ignore

    async with async_session() as session: # type: ignore
        yield session # type: ignore
