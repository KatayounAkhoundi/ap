"""Borrow business logic — Python port of ap.projects.finalproject.BorrowManager."""
from datetime import date, timedelta

import storage
from borrow_record import BorrowRecord
from student_borrow_report import StudentBorrowReport


class BorrowManager:
    def __init__(self):
        self.borrow_records = storage.load_borrow_records()
        if self.borrow_records is None:
            self.borrow_records = []

    def mark_book_as_picked_up(self, student_username, book_isbn):
        record = self.find_ready_for_pickup_record(student_username, book_isbn)
        if record is not None:
            record.mark_as_picked_up()
            self._save_records()
            return True
        return False

    def find_ready_for_pickup_record(self, student_username, book_isbn):
        for record in self.borrow_records:
            if (record.student_username == student_username
                    and record.book_isbn == book_isbn
                    and record.is_ready_for_pickup()):
                return record
        return None

    def get_all_ready_for_pickup_records(self):
        return [record for record in self.borrow_records if record.is_ready_for_pickup()]

    def display_ready_for_pickup_books(self):
        ready_records = self.get_all_ready_for_pickup_records()

        print("\n--- Books Ready for Pickup ---")
        if not ready_records:
            print("No books ready for pickup.")
            return

        for record in ready_records:
            print(record)

    def generate_student_report(self, student_username):
        return StudentBorrowReport(student_username, self.get_student_borrows(student_username))

    def get_all_borrows(self):
        return list(self.borrow_records)

    def get_total_borrows_count(self):
        return len(self.borrow_records)

    def get_borrowed_out_count(self):
        return sum(1 for record in self.borrow_records if record.is_picked_up and not record.is_returned)

    def create_borrow(self, student_username, book_isbn, start_date=None, end_date=None):
        start = start_date if start_date is not None else date.today()
        # Records saved before the end date was stored fall back to a two-week loan.
        end = end_date if end_date is not None else start + timedelta(days=14)
        self.borrow_records.append(BorrowRecord(student_username, book_isbn, start, end))
        self._save_records()

    def return_book(self, student_username, book_isbn):
        record = self.find_active_borrow(student_username, book_isbn)
        if record is not None and record.is_picked_up:
            record.mark_as_returned()
            self._save_records()
            return True
        return False

    def find_active_borrow(self, student_username, book_isbn):
        for record in self.borrow_records:
            if (record.student_username == student_username
                    and record.book_isbn == book_isbn
                    and not record.is_returned):
                return record
        return None

    def get_student_borrows(self, student_username):
        return [record for record in self.borrow_records if record.student_username == student_username]

    def get_active_borrows(self):
        return [record for record in self.borrow_records if not record.is_returned]

    def _save_records(self):
        storage.save_borrow_records(self.borrow_records)
