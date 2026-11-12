# Book
# ID
# title
# description
# authorID
# rating
# file_url UNIQE -> PDF, DOCX


class Book:
    def __init__(self, title, description, file_url, author):
        self.ID = -1
        self.title = title
        self.description = description
        self.file_url = file_url
        self.author = author
