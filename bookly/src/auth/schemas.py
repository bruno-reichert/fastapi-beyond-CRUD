from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime
from src.books.models import Book

class UserCreateModel(BaseModel):
    username: str = Field(max_length = 20)
    email: str = Field(max_length = 40)
    password: str = Field(min_length = 6)
    first_name: str = Field(max_length = 100)
    last_name: str = Field(max_length = 100)

class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    books: list[Book] = []

class UserLoginModel(BaseModel):
    email: str = Field(max_length = 40)
    password: str = Field(min_length = 6)