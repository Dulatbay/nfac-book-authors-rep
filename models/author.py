# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from core.database import Base
#
#
# class AuthorModel(Base):
#     # Класс -> таблица, атрибут -> колонка, экземпляр -> строка
#     __tablename__ = "authors"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     first_name: Mapped[str] = mapped_column(String(64))
#     last_name: Mapped[str] = mapped_column(String(64))
#     username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
#     password_hash: Mapped[str] = mapped_column(String(255))
#     image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
#
#     # One-to-Many: автор -> книги (двусторонняя навигация через back_populates)
#     books: Mapped[list["BookModel"]] = relationship(  # noqa: F821
#         back_populates="author", cascade="all, delete-orphan"
#     )
