# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# import os
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
#
# # SQLite: "sqlite:///./sql_app.db"; Postgres (docker-compose): см. .env.example
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
#
# # check_same_thread=False нужен только SQLite: FastAPI ходит в БД из разных потоков
# connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
#
# # Engine держит пул соединений ("кассы в супермаркете")
# engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
#
# # SessionLocal — фабрика сессий, а не сама сессия
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
#
#
# class Base(DeclarativeBase):
#     """Базовый декларативный класс: через его metadata Alembic видит все модели."""
#
#
# def get_db():
#     """Зависимость: сессия живёт ровно один запрос, затем соединение возвращается в пул."""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
