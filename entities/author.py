from entities.book import Book


class Author:
    def __init__(self, first_name, last_name, image_url):
        self.ID = -1
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url
        self.books = []


    def calculate_rating(self):
        if len(self.books) == 0:
            return 0

        rating = 0
        for book in self.books:
            rating += book.rating

        return rating / len(self.books)