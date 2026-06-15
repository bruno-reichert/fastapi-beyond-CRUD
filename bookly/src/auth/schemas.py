from pydantic import BaseModel, Field, ConfigDict, EmailStr
import uuid
from datetime import datetime
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel
from typing import List

class UserCreateModel(BaseModel):
    username: str = Field(max_length = 20)
    email: EmailStr = Field(max_length = 40)
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

class UserBooksModel(UserResponseModel):
    books: List[Book] = []
    reviews: List[ReviewModel] = []

class UserLoginModel(BaseModel):
    email: EmailStr = Field(max_length = 40)
    password: str = Field(min_length = 6)

class EmailModel(BaseModel):
    addresses: List[str]

class PasswordResetRequestModel(BaseModel):
    email: EmailStr

class PasswordResetConfirmModel(BaseModel):
    new_password: str = Field(min_length = 6)
    confirm_new_password: str = Field(min_length = 6)