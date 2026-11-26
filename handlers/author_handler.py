from fastapi import APIRouter, HTTPException, Response, status

from core.security import CurrentUser
from repositories.author_repository import author_repository
from repositories.book_repository import book_repository
from schemas.author import AuthorCreate, AuthorOut, AuthorUpdate
from schemas.book import BookOut
from schemas.mappers import author_out, book_out
from handlers.auth_handler import register

author_router = APIRouter(prefix="/api/authors", tags=["authors"])


def _get_or_404(author_id: int):
    author = author_repository.get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@author_router.get("", response_model=list[AuthorOut])
def list_authors():
    return [author_out(a) for a in author_repository.get_all()]


@author_router.post("", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate):
    """Алиас регистрации (оставлен для обратной совместимости)."""
    return register(data)


@author_router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int):
    return author_out(_get_or_404(author_id))


@author_router.get("/{author_id}/books", response_model=list[BookOut])
def get_author_books(author_id: int):
    _get_or_404(author_id)
    return [book_out(b) for b in book_repository.get_all(author_id=author_id)]


@author_router.patch("/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, data: AuthorUpdate, user: CurrentUser):
    author = _get_or_404(author_id)
    if author.ID != user.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can edit only your own profile")
    changes = data.model_dump(exclude_unset=True)
    if "image_url" in changes and changes["image_url"] is not None:
        changes["image_url"] = str(changes["image_url"])
    for key, value in changes.items():
        setattr(author, key, value)
    return author_out(author_repository.update(author))


@author_router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, user: CurrentUser):
    author = _get_or_404(author_id)
    if author.ID != user.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own profile")
    for book in list(author.books):
        book_repository.remove(book.ID)
    author_repository.remove(author.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
