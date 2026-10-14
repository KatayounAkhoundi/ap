"""Borrow request model — Python port of ap.projects.finalproject.BorrowRequest."""
from datetime import date, timedelta


class BorrowRequest:
    def __init__(self, student_username, book_isbn, desired_borrow_date, desired_end_date):
        self.student_username = student_username
        self.book_isbn = book_isbn
        self.request_date = date.today()
        self.desired_borrow_date = desired_borrow_date
        self.desired_end_date = desired_end_date
        self.status = "pending"  # "pending", "approved", "rejected"
        self.rejection_reason = ""

    def approve(self):
        self.status = "approved"
        self.rejection_reason = ""

    def reject(self, reason):
        self.status = "rejected"
        self.rejection_reason = reason

    def is_pending(self):
        return self.status == "pending"

    def is_approved(self):
        return self.status == "approved"

    def is_rejected(self):
        return self.status == "rejected"

    def is_approvable_date(self):
        today = date.today()
        return self.desired_borrow_date == today or self.desired_borrow_date == today - timedelta(days=1)

    def __str__(self):
        if self.desired_end_date is not None:
            desired = f"{self.desired_borrow_date} to {self.desired_end_date}"
        else:
            desired = str(self.desired_borrow_date)
        reason = f" | Reason: {self.rejection_reason}" if self.is_rejected() else ""
        return (f"Student: {self.student_username} | Book ISBN: {self.book_isbn} | "
                f"Request Date: {self.request_date} | Desired Period: {desired} | "
                f"Status: {self.status}{reason}")
