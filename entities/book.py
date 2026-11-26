from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.author import Author


@dataclass
class Book:
    title: str
    description: str
    file_url: str  # уникальный, ссылка на PDF/DOCX
    author: Author
    ID: int = -1
    # username оценившего -> оценка 1..5
    ratings: dict[str, int] = field(default_factory=dict)

    @property
    def rating(self) -> float | None:
        if not self.ratings:
            return None
        return round(sum(self.ratings.values()) / len(self.ratings), 2)
