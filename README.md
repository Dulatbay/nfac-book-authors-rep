# Books & Authors API

FastAPI-сервис для авторов и их книг: регистрация, JWT-авторизация, CRUD книг, оценки и простой фронтенд.
Данные пока хранятся **в памяти** (репозитории в `repositories/`) — БД будет подключена позже, интерфейс репозиториев под это готов.

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
export JWT_SECRET_KEY="change-me"   # без него ключ генерируется при каждом старте
uvicorn main:app --reload
```

- Фронтенд: http://localhost:8000/
- Swagger: http://localhost:8000/docs (кнопка Authorize работает)

## Структура

```
core/          конфиг, хеширование паролей, JWT, get_current_user
entities/      доменные модели (dataclass)
schemas/       pydantic-модели запросов/ответов + мапперы
repositories/  in-memory хранилища
handlers/      роутеры: auth, authors, books
static/        фронтенд (vanilla JS)
tests/         pytest
```

## Эндпоинты

| Метод | Путь | Auth | Описание |
|---|---|---|---|
| POST | `/api/auth/register` | — | регистрация автора |
| POST | `/api/auth/login` | — | JSON-логин → JWT |
| GET | `/api/auth/me` | ✔ | текущий пользователь |
| GET | `/api/authors` | — | список авторов (с рейтингом) |
| GET | `/api/authors/{id}` | — | автор |
| GET | `/api/authors/{id}/books` | — | книги автора |
| PATCH/DELETE | `/api/authors/{id}` | ✔ свой | изменить / удалить профиль |
| GET | `/api/books?q=&author_id=` | — | список книг с поиском |
| POST | `/api/books` | ✔ | создать книгу (автор = текущий пользователь) |
| GET | `/api/books/{id}` | — | книга |
| PATCH/DELETE | `/api/books/{id}` | ✔ своя | изменить / удалить |
| POST | `/api/books/{id}/rate` | ✔ | оценка 1–5 (не своей книге) |

## Тесты

```bash
pytest -q
```

## Docker

```bash
cp .env.example .env
docker compose up --build            # app :8000, Postgres :5432, Adminer :8080
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build   # с hot-reload
```

## Подготовка к БД (лекция: SQLAlchemy + Alembic)

Код для БД уже написан, но **закомментирован**, приложение пока работает in-memory.

| Файл | Что внутри |
|---|---|
| `core/database.py` | `DATABASE_URL`, `engine` (пул соединений), `SessionLocal`, `Base`, `get_db` с `yield` |
| `models/` | ORM-модели: `AuthorModel` 1→N `BookModel`, оценки `RatingModel` (M:N автор↔книга) |
| `repositories/sql_*_repository.py` | Repository на Query API: `filter`, `offset/limit`, `add → commit → refresh` |
| `alembic.ini`, `alembic/env.py` | `target_metadata = Base.metadata`, URL из `DATABASE_URL` |
| `alembic/versions/` | первая миграция `initial schema` |

Чтобы включить:
1. Раскомментировать зависимости в `requirements.txt` и файлы выше.
2. В хендлерах заменить in-memory репозитории на `SqlAuthorRepository(db)` / `SqlBookRepository(db)` с `db: Session = Depends(get_db)`. Pydantic-схемы оставить для входа, чтобы не было Mass Assignment.
3. В `docker-compose.yml` раскомментировать `command` с `alembic upgrade head`.

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```
