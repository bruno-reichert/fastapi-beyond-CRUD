from sqlmodel import SQLModel, create_engine, Session, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from src.config import Config
from src.books.models import Book

engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo = True
)

async def init_db():
    async with engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.create_all)