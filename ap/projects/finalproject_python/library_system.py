"""Application core — Python port of ap.projects.finalproject.LibrarySystem."""
from datetime import date, timedelta

from book_manager import BookManager
from borrow_manager import BorrowManager
from borrow_request_manager import BorrowRequestManager
from borrow_statistics import BorrowStatistics
from employee_manager import EmployeeManager
from employee_performance_manager import EmployeePerformanceManager
from menu_handler import MenuHandler
from statistics_manager import StatisticsManager
from student_manager import StudentManager


class LibrarySystem:
    def __init__(self):
        self.student_manager = StudentManager()
        self.book_manager = BookManager()
        self.borrow_manager = BorrowManager()
        self.borrow_request_manager = BorrowRequestManager()
        self.employee_manager = EmployeeManager()
        self.statistics_manager = StatisticsManager(
            self.student_manager, self.book_manager, self.borrow_manager)
        self.performance_manager = EmployeePerformanceManager()
        self.menu_handler = MenuHandler(self)
        self.current_employee = None

    # ---------- Guest ----------

    def display_statistics(self):
        self.statistics_manager.display_statistics()

    def search_books_by_title(self):
        print("\n--- Search Books by Title ---")
        title = input("Enter book title to search: ")

        if not title:
            print("Please enter a title to search.")
            return

        self.book_manager.display_search_results(
            self.book_manager.search_books_by_title(title), False)

    # ---------- Student ----------

    def register_student(self, name, student_id, username, password):
        self.student_manager.register_student(name, student_id, username, password)

    def authenticate_student(self, username, password):
        return self.student_manager.authenticate_student(username, password)

    def search_books_for_student(self):
        self.book_manager.search_books_for_student()

    def display_available_books(self):
        self.book_manager.display_available_books()

    def request_borrow_book(self, student):
        print("\n--- Request to Borrow a Book ---")
        self.book_manager.display_available_books()

        isbn = input("Enter ISBN of the book you want to borrow: ")
        book = self.book_manager.find_book_by_isbn(isbn)
        if book is None:
            print("Invalid ISBN.")
            return
        if not book.is_available:
            print("Book is not available.")
            return

        start_input = input("Enter desired start date (YYYY-MM-DD) or press Enter for today: ")
        start_date = date.today()
        if start_input:
            try:
                start_date = date.fromisoformat(start_input)
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return
        if start_date < date.today():
            print("Start date cannot be in the past.")
            return

        try:
            end_date = date.fromisoformat(input("Enter desired end date (YYYY-MM-DD): "))
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        if end_date <= start_date:
            print("End date must be after the start date.")
            return

        if not student.is_active:
            print("Your account is inactive. You cannot borrow books.")
            return

        self.borrow_request_manager.create_borrow_request(student.username, isbn, start_date, end_date)

    def view_my_borrow_requests(self, student):
        requests = self.borrow_request_manager.get_student_requests(student.username)

        print("\n--- My Borrow Requests ---")
        if not requests:
            print("You have no borrow requests.")
            return

        for request in requests:
            print(request)

    def view_my_borrows(self, student):
        print("\n--- My Borrow History ---")
        borrows = self.borrow_manager.get_student_borrows(student.username)

        if not borrows:
            print("You have no borrow history.")
            return

        for record in borrows:
            print(record)

    def edit_student_information(self, student):
        print("\n--- Edit My Information ---")
        new_name = input(f"New name (current: {student.name}): ")
        new_password = input("New password (press Enter to keep the current one): ")

        if self.student_manager.update_student_info(student.username, new_name, new_password):
            print("Information updated successfully.")
        else:
            print("Nothing to update.")

    # ---------- Employee ----------

    def add_new_book(self):
        if not self._is_employee_logged_in():
            return

        new_book = self.book_manager.create_book_from_input()
        if new_book is not None:
            self.book_manager.add_new_book(new_book)
            self._record_book_added()

    def edit_book(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Edit Book Information ---")
        isbn = input("Enter ISBN of the book to edit: ")

        if self.book_manager.edit_book_from_input(isbn):
            self._record_book_edited()

    def search_books_from_input(self):
        if not self._is_employee_logged_in():
            return

        self.book_manager.search_books_from_input()

    def display_all_books(self):
        self.book_manager.display_all_books()

    def display_pending_approvable_requests(self):
        if not self._is_employee_logged_in():
            return

        self.borrow_request_manager.display_pending_approvable_requests()

    def approve_borrow_request(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Approve Borrow Request ---")
        self.borrow_request_manager.display_pending_approvable_requests()

        username = input("\nEnter student username to approve: ")
        isbn = input("Enter book ISBN to approve: ")

        student = self.student_manager.find_student_by_username(username)
        if student is None:
            print("Student not found.")
            return
        if not student.is_active:
            print("Student is inactive and cannot borrow books.")
            return

        request = self.borrow_request_manager.find_pending_request(username, isbn)
        if request is None:
            print("No pending borrow request found for this student and book.")
            return
        if not request.is_approvable_date():
            print("Only requests whose start date is today or yesterday can be approved.")
            return

        book = self.book_manager.find_book_by_isbn(isbn)
        if book is None:
            print("Invalid ISBN.")
            return
        if not book.is_available:
            print("Book is not available.")
            return

        self.borrow_request_manager.approve_request(request)
        self.book_manager.borrow_book(isbn)
        self.borrow_manager.create_borrow(
            username, isbn, request.desired_borrow_date, request.desired_end_date)
        self._record_borrow_request_approved()
        print("Borrow request approved. The book can now be lent to the student.")

    def reject_borrow_request(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Reject Borrow Request ---")
        self.borrow_request_manager.display_pending_requests()

        username = input("\nEnter student username to reject: ")
        isbn = input("Enter book ISBN to reject: ")
        reason = input("Enter rejection reason: ")

        request = self.borrow_request_manager.find_pending_request(username, isbn)
        if request is None:
            print("No pending borrow request found for this student and book.")
            return

        self.borrow_request_manager.reject_request(request, reason)
        self._record_borrow_request_rejected()
        print("Borrow request rejected successfully!")

    def lend_book_to_student(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Lend Book to Student ---")
        self.borrow_manager.display_ready_for_pickup_books()

        username = input("Enter student username: ")
        isbn = input("Enter book ISBN: ")

        if self.borrow_manager.mark_book_as_picked_up(username, isbn):
            self._record_book_borrowed()
            print("Book handed to the student. Pickup time recorded.")
            record = self.borrow_manager.find_active_borrow(username, isbn)
            if record is not None:
                print(f"Due date: {record.due_date}")
        else:
            print("No approved book ready for pickup found for this student and ISBN.")

    def receive_returned_book(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Receive Returned Book ---")
        borrowed_books = self.borrow_manager.get_active_borrows()
        if not borrowed_books:
            print("No books are currently borrowed.")
            return

        print("\nCurrently borrowed books:")
        for record in borrowed_books:
            print(record)

        username = input("Enter student username: ")
        isbn = input("Enter book ISBN: ")

        if self.borrow_manager.return_book(username, isbn):
            self.book_manager.return_book(isbn)
            self._record_book_returned()
            print("Book received back. Return time recorded.")
        else:
            print("No borrowed book found for this student and ISBN (or it was never picked up).")

    def view_student_borrow_report(self):
        if not self._is_employee_logged_in():
            return

        print("\n=== Student Borrow Report ===")
        username = input("Enter student username: ")

        student = self.student_manager.find_student_by_username(username)
        if student is None:
            print("Student not found.")
            return

        self.borrow_manager.generate_student_report(username).display_report()

    def toggle_student_activation(self):
        if not self._is_employee_logged_in():
            return

        print("\n--- Activate/Deactivate Student ---")
        username = input("Enter student username: ")

        student = self.student_manager.find_student_by_username(username)
        if student is None:
            print("Student not found.")
            return

        if self.student_manager.toggle_student_status(username):
            status = "activated" if student.is_active else "deactivated"
            print(f"Student status updated successfully. Student is now {status}.")
        else:
            print("Failed to update student status.")

    # ---------- Manager ----------

    def register_employee(self, name, employee_id, username, password, role):
        if not self._is_manager_logged_in():
            return

        self.employee_manager.register_employee(name, employee_id, username, password, role)

    def display_all_employees(self):
        if not self._is_manager_logged_in():
            return

        self.employee_manager.display_all_employees()

    def display_all_employees_performance(self):
        if not self._is_manager_logged_in():
            return

        self.performance_manager.display_all_employees_performance()

    def view_borrow_statistics(self):
        if not self._is_manager_logged_in():
            return

        statistics = BorrowStatistics(
            self.borrow_manager.get_all_borrows(),
            self.borrow_request_manager.get_all_requests())
        statistics.display_statistics()

    def display_student_statistics_and_top_late(self):
        if not self._is_manager_logged_in():
            return

        borrows = self.borrow_manager.get_all_borrows()
        self.student_manager.generate_student_statistics(borrows).display_statistics()
        self.student_manager.display_students_with_most_late(10, borrows)

    def display_my_performance(self):
        if not self._is_employee_logged_in():
            return

        self.performance_manager.display_employee_performance(self.current_employee.username)

    # ---------- Authentication ----------

    def authenticate_employee(self, username, password):
        return self.employee_manager.authenticate_employee(username, password)

    def change_employee_password(self, username, current_password, new_password):
        return self.employee_manager.change_password(username, current_password, new_password)

    def set_current_employee(self, employee):
        self.current_employee = employee

    # ---------- Performance recording ----------

    def _record_book_added(self):
        if self.current_employee is not None:
            self.performance_manager.record_book_added(self.current_employee.username)

    def _record_book_edited(self):
        if self.current_employee is not None:
            self.performance_manager.record_book_edited(self.current_employee.username)

    def _record_book_borrowed(self):
        if self.current_employee is not None:
            self.performance_manager.record_book_borrowed(self.current_employee.username)

    def _record_book_returned(self):
        if self.current_employee is not None:
            self.performance_manager.record_book_returned(self.current_employee.username)

    def _record_borrow_request_approved(self):
        if self.current_employee is not None:
            self.performance_manager.record_borrow_request_approved(self.current_employee.username)

    def _record_borrow_request_rejected(self):
        if self.current_employee is not None:
            self.performance_manager.record_borrow_request_rejected(self.current_employee.username)

    # ---------- Guards ----------

    def _is_employee_logged_in(self):
        if self.current_employee is None:
            print("Only employees can perform this action.")
            return False
        return True

    def _is_manager_logged_in(self):
        if self.current_employee is None or not self.current_employee.is_manager():
            print("Only managers can perform this action.")
            return False
        return True

    # ---------- Entry point ----------

    def start(self):
        self.menu_handler.display_main_menu()


if __name__ == "__main__":
    LibrarySystem().start()
