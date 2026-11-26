# ЛЕКЦИЯ: SQLAlchemy + Alembic. Код закомментирован — раскомментировать при подключении БД.

# from sqlalchemy.orm import Session
#
# from models.author import AuthorModel
#
#
# class SqlAuthorRepository:
#     """Repository поверх SQLAlchemy: эндпоинты не знают деталей БД."""
#
#     def __init__(self, db: Session) -> None:
#         self.db = db
#
#     def add(self, author: AuthorModel) -> AuthorModel:
#         self.db.add(author)       # 1. в очередь сессии
#         self.db.commit()          # 2. фиксация транзакции
#         self.db.refresh(author)   # 3. получить сгенерированный id
#         return author
#
#     def update(self, author: AuthorModel) -> AuthorModel:
#         self.db.commit()
#         self.db.refresh(author)
#         return author
#
#     def remove(self, author_id: int) -> bool:
#         author = self.get_by_id(author_id)
#         if author is None:
#             return False
#         self.db.delete(author)
#         self.db.commit()
#         return True
#
#     def get_all(self, offset: int = 0, limit: int = 100) -> list[AuthorModel]:
#         return self.db.query(AuthorModel).offset(offset).limit(limit).all()
#
#     def get_by_id(self, author_id: int) -> AuthorModel | None:
#         return self.db.get(AuthorModel, author_id)
#
#     def get_by_username(self, username: str) -> AuthorModel | None:
#         return self.db.query(AuthorModel).filter(AuthorModel.username == username).first()
