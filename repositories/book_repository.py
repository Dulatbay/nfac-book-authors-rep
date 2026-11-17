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
        for book in self.books:
            if book.ID == book_id:
                self.books.remove(book)
                return True
            return False

    def update_book(self,book):
        for i in self.books:
            if i.ID == book.ID:
                i.title = book.title
                i.description = book.description
                i.file_url = book.file_url
                i.author = book.author
                return i
        return None

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.ID == book_id:
                return book

        return None

book_repository = BookRepository()


