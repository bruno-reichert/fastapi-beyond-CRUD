import asyncio
from src.db.main import async_engine
from sqlmodel import SQLModel

async def main():
    print("Dropping all existing tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    
    print("Creating all tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())
