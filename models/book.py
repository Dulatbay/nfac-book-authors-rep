# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# from sqlalchemy import ForeignKey, Integer, String, Text
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from core.database import Base
#
#
# class BookModel(Base):
#     __tablename__ = "books"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     title: Mapped[str] = mapped_column(String(200), index=True)
#     description: Mapped[str] = mapped_column(Text, default="")
#     file_url: Mapped[str] = mapped_column(String(500), unique=True)
#     author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), index=True)
#
#     author: Mapped["AuthorModel"] = relationship(back_populates="books")  # noqa: F821
#     ratings: Mapped[list["RatingModel"]] = relationship(  # noqa: F821
#         back_populates="book", cascade="all, delete-orphan"
#     )
