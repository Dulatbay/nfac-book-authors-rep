from dataclasses import dataclass, field

from entities.book import Book


@dataclass
class Author:
    first_name: str
    last_name: str
    username: str
    password_hash: str
    image_url: str | None = None
    ID: int = -1
    books: list[Book] = field(default_factory=list)

    def calculate_rating(self) -> float:
        rated = [b.rating for b in self.books if b.rating is not None]
        if not rated:
            return 0.0
        return round(sum(rated) / len(rated), 2)
