"""Book domain model — Python port of ap.projects.finalproject.Book."""


class Book:
    def __init__(self, title, author, publication_year, isbn):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn
        self.is_available = True

    def get_book_info(self):
        return (f"Title: {self.title} | Author: {self.author} | "
                f"Year: {self.publication_year} | ISBN: {self.isbn}")

    def get_full_book_info(self):
        status = "Available" if self.is_available else "Borrowed"
        return (f"Title: {self.title} | Author: {self.author} | "
                f"Year: {self.publication_year} | ISBN: {self.isbn} | "
                f"Status: {status}")

    def __str__(self):
        return self.get_full_book_info()

    def matches_title_search(self, search_title):
        if not search_title:
            return False
        return search_title.lower() in self.title.lower()

    def matches_isbn_search(self, search_isbn):
        if not search_isbn:
            return False
        return search_isbn.lower() in self.isbn.lower()

    def matches_author_search(self, search_author):
        if not search_author:
            return False
        return search_author.lower() in self.author.lower()

    def matches_publication_year(self, year):
        return self.publication_year == year
