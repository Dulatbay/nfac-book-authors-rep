from entities.author import Author


class AuthorRepository:
    """In-memory хранилище авторов (до подключения БД)."""

    def __init__(self) -> None:
        self._next_id = 0
        self._authors: dict[int, Author] = {}

    def add(self, author: Author) -> Author:
        self._next_id += 1
        author.ID = self._next_id
        self._authors[author.ID] = author
        return author

    def update(self, author: Author) -> Author:
        if author.ID not in self._authors:
            raise KeyError(author.ID)
        self._authors[author.ID] = author
        return author

    def remove(self, author_id: int) -> bool:
        return self._authors.pop(author_id, None) is not None

    def get_all(self) -> list[Author]:
        return list(self._authors.values())

    def get_by_id(self, author_id: int) -> Author | None:
        return self._authors.get(author_id)

    def get_by_username(self, username: str) -> Author | None:
        return next((a for a in self._authors.values() if a.username == username), None)

    def clear(self) -> None:
        self._next_id = 0
        self._authors.clear()


author_repository = AuthorRepository()
