from entities.author import Author
from entities.book import Book
from schemas.author import AuthorOut, AuthorShort
from schemas.book import BookOut


def author_short(a: Author) -> AuthorShort:
    return AuthorShort(id=a.ID, first_name=a.first_name, last_name=a.last_name, username=a.username)


def author_out(a: Author) -> AuthorOut:
    return AuthorOut(
        **author_short(a).model_dump(),
        image_url=a.image_url,
        rating=a.calculate_rating(),
        books_count=len(a.books),
    )


def book_out(b: Book) -> BookOut:
    return BookOut(
        id=b.ID,
        title=b.title,
        description=b.description,
        file_url=b.file_url,
        rating=b.rating,
        ratings_count=len(b.ratings),
        author=author_short(b.author),
    )
