# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from core.database import Base
#
#
# class RatingModel(Base):
#     # Many-to-Many авторы <-> книги через ассоциативную таблицу с доп. полем (оценка)
#     __tablename__ = "ratings"
#     __table_args__ = (
#         UniqueConstraint("book_id", "author_id", name="uq_rating_book_author"),
#         CheckConstraint("value BETWEEN 1 AND 5", name="ck_rating_value"),
#     )
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     value: Mapped[int] = mapped_column(Integer)
#     book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
#     author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
#
#     book: Mapped["BookModel"] = relationship(back_populates="ratings")  # noqa: F821
