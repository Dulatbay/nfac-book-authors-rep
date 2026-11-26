from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET
from entities.author import Author
from repositories.author_repository import author_repository

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)


def authenticate(username: str, password: str) -> Author | None:
    author = author_repository.get_by_username(username)
    if author is None or not verify_password(password, author.password_hash):
        return None
    return author


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Author:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    username = payload.get("sub")
    if not username:
        raise credentials_exception
    user = author_repository.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[Author, Depends(get_current_user)]
