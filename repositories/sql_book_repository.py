# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# from sqlalchemy import or_
# from sqlalchemy.orm import Session
#
# from models.book import BookModel
# from models.rating import RatingModel
#
#
# class SqlBookRepository:
#     def __init__(self, db: Session) -> None:
#         self.db = db
#
#     def add(self, book: BookModel) -> BookModel:
#         self.db.add(book)
#         self.db.commit()
#         self.db.refresh(book)
#         return book
#
#     def update(self, book: BookModel) -> BookModel:
#         self.db.commit()
#         self.db.refresh(book)
#         return book
#
#     def remove(self, book_id: int) -> bool:
#         book = self.get_by_id(book_id)
#         if book is None:
#             return False
#         self.db.delete(book)
#         self.db.commit()
#         return True
#
#     def get_all(
#         self, author_id: int | None = None, q: str | None = None, offset: int = 0, limit: int = 100
#     ) -> list[BookModel]:
#         query = self.db.query(BookModel)
#         if author_id is not None:
#             query = query.filter(BookModel.author_id == author_id)
#         if q:
#             like = f"%{q}%"
#             query = query.filter(or_(BookModel.title.ilike(like), BookModel.description.ilike(like)))
#         return query.order_by(BookModel.id).offset(offset).limit(limit).all()
#
#     def get_by_id(self, book_id: int) -> BookModel | None:
#         return self.db.get(BookModel, book_id)
#
#     def get_by_file_url(self, file_url: str) -> BookModel | None:
#         return self.db.query(BookModel).filter(BookModel.file_url == file_url).first()
#
#     def rate(self, book: BookModel, author_id: int, value: int) -> RatingModel:
#         rating = (
#             self.db.query(RatingModel)
#             .filter(RatingModel.book_id == book.id, RatingModel.author_id == author_id)
#             .first()
#         )
#         if rating is None:
#             rating = RatingModel(book_id=book.id, author_id=author_id, value=value)
#             self.db.add(rating)
#         else:
#             rating.value = value
#         self.db.commit()
#         self.db.refresh(book)
#         return rating
