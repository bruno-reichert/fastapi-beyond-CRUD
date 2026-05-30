from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

version = "v1"

app = FastAPI(
    version=version, 
    title="Bookly API", 
    description="A simple API for managing books",
    lifespan=lifespan)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
