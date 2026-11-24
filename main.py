import os
from datetime import timedelta, datetime, UTC
from typing import Annotated

import jwt
from fastapi import FastAPI, Request, Response, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from starlette import status

from dto.AuthCreateRequest import AuthCreateRequest
from dto.AuthLoginRequest import AuthLoginRequest
from entities.Token import Token
from entities.author import Author
from handlers.book_handler import book_router
from entities.TokenData import TokenData
from repositories.author_repository import author_repository

app = FastAPI()


# TODO: add JWT authorization
JWT_SECRET = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()

app.include_router(book_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# register -> login, password -> hash password -> lkdfjgkldfjgweposdcn,vmxnoihfgkwr
# login -> login, <password> -> get user by login
# -> if user exist we need to hash input password
# -> check hashed password in db with hashed password from input

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = author_repository.get_author_by_username(username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/auth/login")
def login(authRequest: AuthLoginRequest, response: Response):
    user = author_repository.get_author_by_username(authRequest.username)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if verify_password(authRequest.password, user.password):
        access_token = create_access_token(data={"sub": user.username})
        token = Token(access_token=access_token, token_type="Bearer")
        return response.body(token)

    raise HTTPException(status_code=401, detail="Incorrect username or password")

# TODO: reformat to routes
@app.get("/api/authors")
async def get_authors(request: Request):
    authors = author_repository.get_authors()
    return {"authors": authors}

@app.get("/api/authors/{id}")
async def get_author(id: int):
    author = author_repository.get_author_by_id(id)
    return author


# TODO: reformat to basemodel
@app.post("/api/authors")
async def create_author(response: Response,
                        authRequest: AuthCreateRequest):
    author = Author(authRequest)
    author_repository.add(author)

    response.status_code = status.HTTP_201_CREATED
    return response



# TODO: frontend