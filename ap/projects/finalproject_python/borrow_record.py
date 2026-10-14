"""Borrow record model — Python port of ap.projects.finalproject.BorrowRecord."""
from datetime import date


class BorrowRecord:
    def __init__(self, student_username, book_isbn, borrow_date, due_date):
        self.student_username = student_username
        self.book_isbn = book_isbn
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.is_returned = False
        self.is_picked_up = False
        self.return_date = None
        self.actual_pickup_date = None

    def mark_as_picked_up(self):
        self.is_picked_up = True
        self.actual_pickup_date = date.today()

    def mark_as_returned(self):
        self.is_returned = True
        self.return_date = date.today()

    def is_overdue(self):
        return self.is_picked_up and not self.is_returned and date.today() > self.due_date

    def is_returned_late(self):
        return (self.is_returned and self.return_date is not None
                and self.due_date is not None and self.return_date > self.due_date)

    def is_late(self):
        return self.is_returned_late() or self.is_overdue()

    def is_ready_for_pickup(self):
        return not self.is_picked_up and not self.is_returned

    def get_days_overdue(self):
        if not self.is_overdue():
            return 0
        return (date.today() - self.due_date).days

    def __str__(self):
        if self.is_returned:
            if self.is_returned_late():
                status = f"Returned late on {self.return_date.isoformat()}"
            else:
                status = f"Returned on {self.return_date.isoformat()}"
        elif self.is_picked_up:
            if self.is_overdue():
                status = f"OVERDUE ({self.get_days_overdue()} days)"
            else:
                status = f"Due on {self.due_date.isoformat()}"
        else:
            status = "Ready for pickup"

        picked_up = ""
        if self.actual_pickup_date is not None:
            picked_up = f" | Picked up: {self.actual_pickup_date.isoformat()}"

        return (f"Book ISBN: {self.book_isbn} | "
                f"Borrowed: {self.borrow_date.isoformat()} | "
                f"Due: {self.due_date.isoformat()}{picked_up} | "
                f"Status: {status}")
