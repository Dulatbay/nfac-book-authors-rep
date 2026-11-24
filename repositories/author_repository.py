# TODO: add type
class AuthorRepository:
    def __init__(self):
        self.ID = 0
        self.authors = []
        pass


    def add(self, author):
        self.ID += 1
        author.ID = self.ID
        self.authors.append(author)

    def update(self, author):
        pass

    def remove(self, ID):
        pass

    def get_authors(self):
        return self.authors

    def get_author_by_id(self, ID: int):
        print("ID", ID)
        print("authors", self.authors)
        for i in self.authors:
            print("i.id", i.ID, i.ID == ID)
            if +i.ID == +ID:
                return i
        return None

    def get_author_by_username(self, username: str):
        for i in self.authors:
            if i.username == username:
                return i
        return None


author_repository = AuthorRepository()

