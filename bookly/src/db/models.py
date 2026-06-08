from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date
from typing import Optional

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import Optional
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    books: Optional[list["Book"]] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: Optional[list["Review"]] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<User {self.username}>"
    
class Book(SQLModel, table=True):
    __tablename__ = "books" # type: ignore

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: Optional[list["Review"]] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
    
class Review(SQLModel, table=True):
    __tablename__ = "reviews" # type: ignore

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(ge=1, le=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")
    def __repr__(self):
        return f"<Review {self.rating} stars by {self.user_uid} for {self.book_uid}>"