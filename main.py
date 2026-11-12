from fastapi import FastAPI, Request, Response, Form
from starlette import status

from entities.author import Author
from handlers.book_handler import book_router
from repositories.author_repository import author_repository

app = FastAPI()


app.include_router(book_router)

@app.get("/api/authors")
async def get_authors(request: Request):
    authors = author_repository.get_authors()
    return {"authors": authors}

@app.get("/api/authors/{id}")
async def get_author(id: int):
    author = author_repository.get_author_by_id(id)
    return author


@app.post("/api/authors")
async def create_author(response: Response,
                        first_name: str = Form(...),
                        last_name: str = Form(...),
                        image_url: str = Form(...)):
    author = Author(first_name=first_name, last_name=last_name, image_url=image_url)
    author_repository.add(author)

    response.status_code = status.HTTP_201_CREATED
    return response

