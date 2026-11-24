from dto.AuthCreateRequest import AuthCreateRequest
from entities.book import Book


class Author:
    def __init__(self, authRequest: AuthCreateRequest):
        self.ID = -1
        self.first_name = authRequest.first_name
        self.last_name = authRequest.last_name
        self.image_url = authRequest.image_url
        self.books = []
        self.password = authRequest.password
        self.username = authRequest.username


    def calculate_rating(self):
        if len(self.books) == 0:
            return 0

        rating = 0
        for book in self.books:
            rating += book.rating

        return rating / len(self.books)