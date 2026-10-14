"""Employee performance tracking — Python port of ap.projects.finalproject.EmployeePerformanceManager."""
import storage
from employee_performance import EmployeePerformance


class EmployeePerformanceManager:
    def __init__(self):
        self.performance_records = storage.load_performance_records()
        if self.performance_records is None:
            self.performance_records = {}

    def get_employee_performance(self, employee_username):
        if employee_username not in self.performance_records:
            self.performance_records[employee_username] = EmployeePerformance(employee_username)
        return self.performance_records[employee_username]

    def record_book_added(self, employee_username):
        self.get_employee_performance(employee_username).increment_books_added()
        self._save_records()

    def record_book_edited(self, employee_username):
        self.get_employee_performance(employee_username).increment_books_edited()
        self._save_records()

    def record_book_borrowed(self, employee_username):
        self.get_employee_performance(employee_username).increment_books_borrowed()
        self._save_records()

    def record_book_returned(self, employee_username):
        self.get_employee_performance(employee_username).increment_books_returned()
        self._save_records()

    def record_borrow_request_approved(self, employee_username):
        self.get_employee_performance(employee_username).increment_borrow_requests_approved()
        self._save_records()

    def record_borrow_request_rejected(self, employee_username):
        self.get_employee_performance(employee_username).increment_borrow_requests_rejected()
        self._save_records()

    def display_employee_performance(self, employee_username):
        self.get_employee_performance(employee_username).display_performance()

    def display_all_employees_performance(self):
        print("\n=== All Employees Performance Report ===")
        if not self.performance_records:
            print("No performance records found.")
            return

        for performance in self.performance_records.values():
            print(f"\n{performance}")

    def get_top_performers(self, limit):
        return sorted(self.performance_records.values(),
                      key=lambda p: p.get_total_activities(),
                      reverse=True)[:limit]

    def display_top_performers(self, limit):
        top_performers = self.get_top_performers(limit)

        print(f"\n=== Top {limit} Performers ===")
        if not top_performers:
            print("No performance records found.")
            return

        for i, performance in enumerate(top_performers, start=1):
            print(f"{i}. {performance}")

    def _save_records(self):
        storage.save_performance_records(self.performance_records)
