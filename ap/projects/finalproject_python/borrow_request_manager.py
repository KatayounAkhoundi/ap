"""Borrow request business logic — Python port of ap.projects.finalproject.BorrowRequestManager."""
import storage
from borrow_request import BorrowRequest


class BorrowRequestManager:
    def __init__(self):
        self.borrow_requests = storage.load_borrow_requests()
        if self.borrow_requests is None:
            self.borrow_requests = []

    def create_borrow_request(self, student_username, book_isbn, desired_borrow_date, desired_end_date):
        if self.find_pending_request(student_username, book_isbn) is not None:
            print("You already have a pending request for this book.")
            return

        request = BorrowRequest(student_username, book_isbn, desired_borrow_date, desired_end_date)
        self.borrow_requests.append(request)
        self._save_requests()
        print("Borrow request submitted successfully. Waiting for approval.")

    def get_all_requests(self):
        return list(self.borrow_requests)

    def get_pending_requests(self):
        return [request for request in self.borrow_requests if request.is_pending()]

    def get_pending_approvable_requests(self):
        return [request for request in self.borrow_requests
                if request.is_pending() and request.is_approvable_date()]

    def get_student_requests(self, student_username):
        return [request for request in self.borrow_requests
                if request.student_username == student_username]

    def find_pending_request(self, student_username, book_isbn):
        for request in self.borrow_requests:
            if (request.student_username == student_username
                    and request.book_isbn == book_isbn
                    and request.is_pending()):
                return request
        return None

    def approve_request(self, request):
        request.approve()
        self._save_requests()

    def reject_request(self, request, reason):
        request.reject(reason)
        self._save_requests()

    def display_pending_requests(self):
        pending_requests = self.get_pending_requests()

        print("\n--- Pending Borrow Requests ---")
        if not pending_requests:
            print("No pending borrow requests.")
            return

        for request in pending_requests:
            print(request)

    def display_pending_approvable_requests(self):
        approvable_requests = self.get_pending_approvable_requests()

        print("\n--- Pending Borrow Requests (Start Date: Today or Yesterday) ---")
        if not approvable_requests:
            print("No pending borrow requests to approve today.")
            return

        for request in approvable_requests:
            print(request)

    def _save_requests(self):
        storage.save_borrow_requests(self.borrow_requests)
