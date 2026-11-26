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
