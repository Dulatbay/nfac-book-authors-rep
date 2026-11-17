from fastapi import APIRouter, Form, Response, status

from entities.book import Book
from repositories.author_repository import author_repository
from repositories.book_repository import book_repository

book_router = APIRouter()

@book_router.post("/api/books", tags=["books"])
async def create_book(response: Response,
                    title: str = Form(...),
                    description: str = Form(...),
                    authorID: int = Form(...),
                    file_url: str = Form(...)):
    author = author_repository.get_author_by_id(authorID)

    if author is None:
        return {"message": "Author not found"}, 404

    book = Book(title=title, description=description, author=author, file_url=file_url)
    book_repository.add_book(book)

    response.status_code = status.HTTP_201_CREATED
    return response


@book_router.get("/api/books", tags=["books"])
async def get_books():
    books = book_repository.get_books()
    return {"books": books}


@book_router.get("/api/books/{id}", tags=["books"])
async def get_book(id: int):
    book = book_repository.get_book_by_id(id)
    return book

@book_router.delete("/api/books/{id}", tags=["books"])
async def delete_book(id: int):
    result = book_repository.delete_book(id)
    if result:
        return {"message": "Book deleted"}
    return {"message": "Book not found"}

@book_router.put("/api/books/{id}", tags=["books"])
async def update_book(
    id: int,
    title: str,
    description: str,
    authorID: int,
    file_url: str
):
    author = author_repository.get_author_by_id(authorID)
    if author is None:
        return {"message": "Author not found"}
    book = Book(
        title=title,
        description=description,
        author=author,
        file_url=file_url
    )
    book.ID = id
    updated_book = book_repository.update_book(book)
    if updated_book:
        return {"message": "Book updated"}
    return {"message": "Book not found"}