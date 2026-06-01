from pydantic import BaseModel, Field

from src.auth.models import User

class UserCreateModel(BaseModel):
    username: str = Field(max_length = 20)
    email: str = Field(max_length = 40)
    password: str = Field(min_length = 6)
    first_name: str = Field(max_length = 100)
    last_name: str = Field(max_length = 100)

class UserResponseModel(User):
    pass