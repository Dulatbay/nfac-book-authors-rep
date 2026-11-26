from pydantic import BaseModel, Field, HttpUrl

from schemas.author import AuthorShort


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    file_url: HttpUrl


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    file_url: HttpUrl | None = None


class RateRequest(BaseModel):
    rating: int = Field(ge=1, le=5)


class BookOut(BaseModel):
    id: int
    title: str
    description: str
    file_url: str
    rating: float | None
    ratings_count: int
    author: AuthorShort
