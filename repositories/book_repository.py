# TODO: add type
class BookRepository:
    def __init__(self):
        self.ID = 0
        self.books = []


    def add_book(self, book):
        self.ID += 1
        book.ID = self.ID
        self.books.append(book)

    def get_books(self):
        return self.books

    def delete_book(self, book):
        pass

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.ID == book_id:
                return book

        return None

book_repository = BookRepository()


