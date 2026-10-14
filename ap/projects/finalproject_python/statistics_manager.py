"""Library-wide statistics — Python port of ap.projects.finalproject.StatisticsManager."""


class StatisticsManager:
    def __init__(self, student_manager, book_manager, borrow_manager):
        self.student_manager = student_manager
        self.book_manager = book_manager
        self.borrow_manager = borrow_manager

    def display_statistics(self):
        print("\n=== Library Statistics ===")
        print(f"Registered Students: {self.student_manager.get_student_count()}")
        print(f"Total Books: {self.book_manager.get_total_books_count()}")
        print(f"Total Borrows: {self.borrow_manager.get_total_borrows_count()}")
        print(f"Books Currently Borrowed: {self.borrow_manager.get_borrowed_out_count()}")
