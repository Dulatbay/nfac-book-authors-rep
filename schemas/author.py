from pydantic import BaseModel, Field, HttpUrl

from schemas.auth import USERNAME_PATTERN


class AuthorCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    username: str = Field(min_length=3, max_length=32, pattern=USERNAME_PATTERN)
    password: str = Field(min_length=6, max_length=128)
    image_url: HttpUrl | None = None


class AuthorUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=64)
    last_name: str | None = Field(default=None, min_length=1, max_length=64)
    image_url: HttpUrl | None = None


class AuthorShort(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str


class AuthorOut(AuthorShort):
    image_url: str | None
    rating: float
    books_count: int
