from fastapi import APIRouter, status
from schemas import BookCreateSchema, BookSavedSchema

from storage import storage

api_router = APIRouter(
    prefix='/api/books'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    saved_book = storage.create_book(book)

    return saved_book


@api_router.get("/{book_id}")
def get_book(book_id: str) -> BookSavedSchema:
    saved_book = storage.get_book(book_id)

    return saved_book