"""Book business logic — Python port of ap.projects.finalproject.BookManager."""
import book_file_manager
from book import Book


class BookManager:
    def __init__(self):
        self.books = book_file_manager.load_books()
        if self.books is None:
            self.books = []

    def search_books(self, title, author, year, isbn):
        return [
            book for book in self.books
            if (not title or book.matches_title_search(title))
            and (not author or book.matches_author_search(author))
            and (year is None or book.matches_publication_year(year))
            and (not isbn or book.matches_isbn_search(isbn))
        ]

    def search_books_by_title(self, title):
        if not title:
            return []
        return self.search_books(title, None, None, None)

    def edit_book(self, isbn, new_title, new_author, new_year):
        book = self.find_book_by_isbn(isbn)
        if book is None:
            return False
        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
        if new_year is not None and new_year > 0:
            book.publication_year = new_year
        self._save_books()
        return True

    def edit_book_from_input(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if book is None:
            print(f"Book with ISBN {isbn} not found.")
            return False

        print("\nCurrent book information:")
        print(book.get_full_book_info())
        print("\nEnter new information (press Enter to keep current value):")

        new_title = input(f"New title (current: {book.title}): ")
        new_author = input(f"New author (current: {book.author}): ")

        new_year = None
        year_input = input(f"New publication year (current: {book.publication_year}): ")
        if year_input:
            try:
                new_year = int(year_input)
                if new_year < 1000 or new_year > 2100:
                    print("Invalid year. Must be between 1000 and 2100.")
                    return False
            except ValueError:
                print("Invalid year format.")
                return False

        if self.edit_book(isbn, new_title, new_author, new_year):
            print("Book information updated successfully!")
            print(self.find_book_by_isbn(isbn).get_full_book_info())
            return True
        print("Failed to update book information.")
        return False

    def search_books_from_input(self):
        print("\n--- Advanced Book Search ---")
        title = input("Title (press Enter to skip): ")
        author = input("Author (press Enter to skip): ")
        year = self._read_optional_year()
        isbn = input("ISBN (press Enter to skip): ")

        self.display_search_results(self.search_books(title, author, year, isbn), True)

    def search_books_for_student(self):
        print("\n--- Book Search ---")
        title = input("Title (press Enter to skip): ")
        author = input("Author (press Enter to skip): ")
        year = self._read_optional_year()

        self.display_search_results(self.search_books(title, author, year, None), True)

    def add_new_book(self, book):
        if self._is_isbn_taken(book.isbn):
            print("A book with this ISBN already exists.")
            return

        self.books.append(book)
        self._save_books()
        print("Book added successfully!")

    def _is_isbn_taken(self, isbn):
        return any(book.isbn == isbn for book in self.books)

    def create_book_from_input(self):
        print("\n--- Add New Book ---")

        title = input("Book title: ")
        author = input("Author: ")
        year = self._get_int_input(1000, 2100, prompt="Publication year: ")
        isbn = input("ISBN: ")

        if not isbn or len(isbn) < 10:
            print("Invalid ISBN. Please enter a valid ISBN (minimum 10 characters).")
            return None

        return Book(title, author, year, isbn)

    @staticmethod
    def _read_optional_year():
        year_input = input("Publication year (press Enter to skip): ")
        if not year_input:
            return None
        try:
            return int(year_input)
        except ValueError:
            print("Invalid year format, ignoring the year filter.")
            return None

    @staticmethod
    def _get_int_input(min_value, max_value, prompt):
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                print(f"Please enter a number between {min_value} and {max_value}: ", end="")
            except ValueError:
                print("Invalid input. Please enter a number: ", end="")

    def get_total_books_count(self):
        return len(self.books)

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all_books(self):
        print("\n--- All Books in Library ---")
        if not self.books:
            print("No books available in the library.")
            return

        for book in self.books:
            print(book.get_full_book_info())

    def display_available_books(self):
        print("\n--- Available Books ---")
        available_books = [book for book in self.books if book.is_available]

        if not available_books:
            print("No books available at the moment.")
            return

        for book in available_books:
            print(book.get_book_info())

    def display_search_results(self, results, include_status):
        if not results:
            print("No books found matching your criteria.")
            return

        print("\n--- Search Results ---")
        for book in results:
            print(book.get_full_book_info() if include_status else book.get_book_info())
        print(f"Found {len(results)} book(s)")

    def borrow_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if book is not None and book.is_available:
            book.is_available = False
            self._save_books()
            return True
        return False

    def return_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if book is not None and not book.is_available:
            book.is_available = True
            self._save_books()
            return True
        return False

    def _save_books(self):
        book_file_manager.save_books(self.books)
