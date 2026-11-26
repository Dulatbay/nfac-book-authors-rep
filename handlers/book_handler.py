from fastapi import APIRouter, HTTPException, Response, status

from core.security import CurrentUser
from entities.book import Book
from repositories.book_repository import book_repository
from schemas.book import BookCreate, BookOut, BookUpdate, RateRequest
from schemas.mappers import book_out

book_router = APIRouter(prefix="/api/books", tags=["books"])


def _get_or_404(book_id: int) -> Book:
    book = book_repository.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


def _ensure_unique_file(file_url: str, exclude_id: int | None = None) -> None:
    existing = book_repository.get_by_file_url(file_url)
    if existing and existing.ID != exclude_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book with this file_url already exists")


@book_router.get("", response_model=list[BookOut])
def list_books(author_id: int | None = None, q: str | None = None):
    books = book_repository.get_all(author_id=author_id)
    if q:
        needle = q.lower()
        books = [b for b in books if needle in b.title.lower() or needle in b.description.lower()]
    return [book_out(b) for b in books]


@book_router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, user: CurrentUser):
    file_url = str(data.file_url)
    _ensure_unique_file(file_url)
    book = Book(title=data.title, description=data.description, file_url=file_url, author=user)
    return book_out(book_repository.add(book))


@book_router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    return book_out(_get_or_404(book_id))


@book_router.patch("/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookUpdate, user: CurrentUser):
    book = _get_or_404(book_id)
    if book.author.ID != user.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can edit only your own books")
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if "file_url" in changes:
        changes["file_url"] = str(changes["file_url"])
        _ensure_unique_file(changes["file_url"], exclude_id=book.ID)
    for key, value in changes.items():
        setattr(book, key, value)
    return book_out(book_repository.update(book))


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, user: CurrentUser):
    book = _get_or_404(book_id)
    if book.author.ID != user.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own books")
    book_repository.remove(book.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@book_router.post("/{book_id}/rate", response_model=BookOut)
def rate_book(book_id: int, data: RateRequest, user: CurrentUser):
    book = _get_or_404(book_id)
    if book.author.ID == user.ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot rate your own book")
    book.ratings[user.username] = data.rating
    return book_out(book)
