"""Employee performance model — Python port of ap.projects.finalproject.EmployeePerformance."""
from datetime import date


class EmployeePerformance:
    def __init__(self, employee_username):
        self.employee_username = employee_username
        self.books_added = 0
        self.books_edited = 0
        self.books_borrowed = 0
        self.books_returned = 0
        self.borrow_requests_approved = 0
        self.borrow_requests_rejected = 0
        self.last_activity_date = date.today()

    def _touch(self):
        self.last_activity_date = date.today()

    def increment_books_added(self):
        self.books_added += 1
        self._touch()

    def increment_books_edited(self):
        self.books_edited += 1
        self._touch()

    def increment_books_borrowed(self):
        self.books_borrowed += 1
        self._touch()

    def increment_books_returned(self):
        self.books_returned += 1
        self._touch()

    def increment_borrow_requests_approved(self):
        self.borrow_requests_approved += 1
        self._touch()

    def increment_borrow_requests_rejected(self):
        self.borrow_requests_rejected += 1
        self._touch()

    def get_total_activities(self):
        return (self.books_added + self.books_edited + self.books_borrowed
                + self.books_returned + self.borrow_requests_approved
                + self.borrow_requests_rejected)

    def __str__(self):
        return (f"Employee: {self.employee_username} | Books Added: {self.books_added} | "
                f"Books Edited: {self.books_edited} | Books Lent: {self.books_borrowed} | "
                f"Books Received Back: {self.books_returned} | "
                f"Requests Approved: {self.borrow_requests_approved} | "
                f"Requests Rejected: {self.borrow_requests_rejected} | "
                f"Last Activity: {self.last_activity_date} | "
                f"Total Activities: {self.get_total_activities()}")

    def display_performance(self):
        print("\n=== Employee Performance Report ===")
        print(f"Employee: {self.employee_username}")
        print(f"Books Added: {self.books_added}")
        print(f"Books Edited: {self.books_edited}")
        print(f"Books Lent: {self.books_borrowed}")
        print(f"Books Received Back: {self.books_returned}")
        print(f"Borrow Requests Approved: {self.borrow_requests_approved}")
        print(f"Borrow Requests Rejected: {self.borrow_requests_rejected}")
        print(f"Total Activities: {self.get_total_activities()}")
        print(f"Last Activity Date: {self.last_activity_date}")
