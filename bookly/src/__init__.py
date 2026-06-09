from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.tags.routes import tags_router
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import *

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
    description="A simple API for managing books")

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])