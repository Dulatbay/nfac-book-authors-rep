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
        for i in self.authors:
            if i.ID==author.ID:
                i.first_name = author.first_name
                i.last_name = author.last_name
                i.image_url = author.image_url
                return i
            return None
        
    def remove(self, ID):
        for author in self.authors:
            if author.ID == ID:
                self.authors.remove(author)
                return True
            return False

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



author_repository = AuthorRepository()

