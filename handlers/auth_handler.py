from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import CurrentUser, authenticate, create_access_token, get_password_hash
from entities.author import Author
from repositories.author_repository import author_repository
from schemas.auth import LoginRequest, Token
from schemas.author import AuthorCreate, AuthorOut
from schemas.mappers import author_out

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


def _issue_token(username: str, password: str) -> Token:
    author = authenticate(username, password)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token({"sub": author.username}))


@auth_router.post("/register", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def register(data: AuthorCreate):
    if author_repository.get_by_username(data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    author = Author(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        password_hash=get_password_hash(data.password),
        image_url=str(data.image_url) if data.image_url else None,
    )
    return author_out(author_repository.add(author))


@auth_router.post("/login", response_model=Token)
def login(data: LoginRequest):
    return _issue_token(data.username, data.password)


@auth_router.post("/token", response_model=Token, include_in_schema=False)
def token(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Form-эндпоинт для кнопки Authorize в Swagger UI."""
    return _issue_token(form.username, form.password)


@auth_router.get("/me", response_model=AuthorOut)
def me(user: CurrentUser):
    return author_out(user)
