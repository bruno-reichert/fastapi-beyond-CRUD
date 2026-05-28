from fastapi import Header, status, APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from .schemas import Book, BookUpdateModel
from .book_data import books

book_router = APIRouter()

@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get("/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book.update(book_update_data.model_dump(exclude_unset=True))
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")