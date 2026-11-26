from entities.book import Book


class BookRepository:
    """In-memory хранилище книг (до подключения БД)."""

    def __init__(self) -> None:
        self._next_id = 0
        self._books: dict[int, Book] = {}

    def add(self, book: Book) -> Book:
        self._next_id += 1
        book.ID = self._next_id
        self._books[book.ID] = book
        book.author.books.append(book)
        return book

    def update(self, book: Book) -> Book:
        if book.ID not in self._books:
            raise KeyError(book.ID)
        self._books[book.ID] = book
        return book

    def remove(self, book_id: int) -> bool:
        book = self._books.pop(book_id, None)
        if book is None:
            return False
        if book in book.author.books:
            book.author.books.remove(book)
        return True

    def get_all(self, author_id: int | None = None) -> list[Book]:
        books = list(self._books.values())
        if author_id is not None:
            books = [b for b in books if b.author.ID == author_id]
        return books

    def get_by_id(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def get_by_file_url(self, file_url: str) -> Book | None:
        return next((b for b in self._books.values() if b.file_url == file_url), None)

    def clear(self) -> None:
        self._next_id = 0
        self._books.clear()


book_repository = BookRepository()
