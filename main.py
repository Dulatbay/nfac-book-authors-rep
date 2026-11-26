from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from handlers.auth_handler import auth_router
from handlers.author_handler import author_router
from handlers.book_handler import book_router

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Books & Authors API", version="1.0.0")

app.include_router(auth_router)
app.include_router(author_router)
app.include_router(book_router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")
