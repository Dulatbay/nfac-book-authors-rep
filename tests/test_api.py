import pytest
from fastapi.testclient import TestClient

from main import app
from repositories.author_repository import author_repository
from repositories.book_repository import book_repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean():
    author_repository.clear()
    book_repository.clear()


def register(username="alice", password="secret1"):
    r = client.post("/api/auth/register", json={
        "first_name": "A", "last_name": "B", "username": username, "password": password,
    })
    assert r.status_code == 201, r.text
    return r.json()


def auth(username="alice", password="secret1"):
    r = client.post("/api/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_register_hides_password_and_rejects_duplicates():
    data = register()
    assert "password" not in data and "password_hash" not in data
    dup = {"first_name": "A", "last_name": "B", "username": "alice", "password": "secret1"}
    r = client.post("/api/auth/register", json=dup)
    assert r.status_code == 409


def test_validation():
    r = client.post("/api/auth/register", json={"first_name": "A", "last_name": "B", "username": "a!", "password": "1"})
    assert r.status_code == 422


def test_login_and_me():
    register()
    assert client.post("/api/auth/login", json={"username": "alice", "password": "wrong12"}).status_code == 401
    r = client.get("/api/auth/me", headers=auth())
    assert r.json()["username"] == "alice"
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer junk"}).status_code == 401


def test_books_crud_and_rating():
    register()
    register("bob")
    h_alice, h_bob = auth(), auth("bob")
    payload = {"title": "Book", "description": "d", "file_url": "https://x.com/a.pdf"}

    assert client.post("/api/books", json=payload).status_code == 401
    book = client.post("/api/books", json=payload, headers=h_alice).json()
    assert book["author"]["username"] == "alice"
    assert client.post("/api/books", json=payload, headers=h_alice).status_code == 409

    assert client.patch(f"/api/books/{book['id']}", json={"title": "X"}, headers=h_bob).status_code == 403
    assert client.patch(f"/api/books/{book['id']}", json={"title": "X"}, headers=h_alice).json()["title"] == "X"

    assert client.post(f"/api/books/{book['id']}/rate", json={"rating": 5}, headers=h_alice).status_code == 400
    r = client.post(f"/api/books/{book['id']}/rate", json={"rating": 4}, headers=h_bob)
    assert r.json()["rating"] == 4
    author = client.get(f"/api/authors/{book['author']['id']}").json()
    assert author["rating"] == 4 and author["books_count"] == 1

    assert client.get("/api/books?q=x").json()[0]["id"] == book["id"]
    assert client.delete(f"/api/books/{book['id']}", headers=h_alice).status_code == 204
    assert client.get(f"/api/books/{book['id']}").status_code == 404


def test_author_update_delete():
    a = register()
    register("bob")
    assert client.patch(f"/api/authors/{a['id']}", json={"first_name": "Z"}, headers=auth("bob")).status_code == 403
    assert client.patch(f"/api/authors/{a['id']}", json={"first_name": "Z"}, headers=auth()).json()["first_name"] == "Z"
    assert client.get("/api/authors/999").status_code == 404
    assert client.delete(f"/api/authors/{a['id']}", headers=auth()).status_code == 204
    assert len(client.get("/api/authors").json()) == 1


def test_frontend_served():
    assert "Books & Authors" in client.get("/").text
