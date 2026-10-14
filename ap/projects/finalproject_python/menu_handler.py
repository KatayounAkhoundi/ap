"""Console menus — Python port of ap.projects.finalproject.MenuHandler."""


class MenuHandler:
    def __init__(self, library_system):
        self.library_system = library_system
        self.current_user = None
        self.current_employee = None

    def display_main_menu(self):
        options = [
            ("Student Login", self.handle_student_login),
            ("Employee Login", self.handle_employee_login),
            ("View Library Statistics", self.library_system.display_statistics),
            ("Search Books by Title", self.library_system.search_books_by_title),
            ("Student Registration", self.handle_student_registration),
            ("Exit", lambda: print("Exiting system. Goodbye!")),
        ]

        while True:
            print("\n=== University Library Management System ===")
            self._print_options(options)
            choice = self._get_int_input(1, len(options))
            options[choice - 1][1]()
            if choice == len(options):
                return
            print("___________________________")

    def handle_student_login(self):
        print("\n--- Student Login ---")
        username = input("Username: ")
        password = input("Password: ")

        self.current_user = self.library_system.authenticate_student(username, password)
        if self.current_user is not None:
            print(f"Login successful! Welcome, {self.current_user.name}")
            self.display_logged_in_student_menu()
        else:
            print("Invalid username or password. Please try again.")

    def handle_student_registration(self):
        print("\n--- New Student Registration ---")
        name = input("Student name: ")
        student_id = input("Student ID: ")
        username = input("Username: ")
        password = input("Password: ")

        self.library_system.register_student(name, student_id, username, password)

    def handle_employee_login(self):
        print("\n--- Employee Login ---")
        username = input("Username: ")
        password = input("Password: ")

        self.current_employee = self.library_system.authenticate_employee(username, password)
        if self.current_employee is not None:
            print(f"Login successful! Welcome, {self.current_employee.name}")
            self.library_system.set_current_employee(self.current_employee)
            self.display_logged_in_employee_menu()
        else:
            print("Invalid username or password. Please try again.")

    def display_logged_in_student_menu(self):
        library = self.library_system
        options = [
            ("View My Information", self._view_my_information),
            ("Edit My Information", lambda: library.edit_student_information(self.current_user)),
            ("Search Books", library.search_books_for_student),
            ("View Available Books", library.display_available_books),
            ("Request to Borrow a Book", lambda: library.request_borrow_book(self.current_user)),
            ("View My Borrow Requests", lambda: library.view_my_borrow_requests(self.current_user)),
            ("View My Borrow History", lambda: library.view_my_borrows(self.current_user)),
            ("Logout", self._logout_student),
        ]

        while self.current_user is not None:
            print("\n=== Student Dashboard ===")
            self._print_options(options)
            choice = self._get_int_input(1, len(options))
            options[choice - 1][1]()
            print("___________________________")
        print("Logged out successfully.")

    def _view_my_information(self):
        print("\n--- My Information ---")
        print(self.current_user)

    def _logout_student(self):
        self.current_user = None

    def display_logged_in_employee_menu(self):
        options = self._build_employee_options()
        while self.current_employee is not None:
            manager_suffix = " (Manager)" if self.current_employee.is_manager() else ""
            print(f"\n=== Employee Dashboard{manager_suffix} ===")
            self._print_options(options)
            choice = self._get_int_input(1, len(options))
            options[choice - 1][1]()
            print("___________________________")
        print("Logged out successfully.")

    def _build_employee_options(self):
        library = self.library_system
        options = [
            ("Add New Book", library.add_new_book),
            ("Search Books", library.search_books_from_input),
            ("View Available Books", library.display_available_books),
            ("View All Books", library.display_all_books),
            ("Edit Book Information", library.edit_book),
            ("View Pending Borrow Requests (Start Date: Today/Yesterday)",
             library.display_pending_approvable_requests),
            ("Approve Borrow Request", library.approve_borrow_request),
            ("Reject Borrow Request", library.reject_borrow_request),
            ("Lend Book to Student (Record Pickup)", library.lend_book_to_student),
            ("Receive Returned Book (Record Return Time)", library.receive_returned_book),
            ("Student Borrow Report", library.view_student_borrow_report),
            ("Activate/Deactivate Student", library.toggle_student_activation),
            ("View My Performance", library.display_my_performance),
            ("Change Password", self.handle_change_password),
        ]

        if self.current_employee.is_manager():
            options.extend([
                ("Register New Employee", self.handle_employee_registration),
                ("View All Employees", library.display_all_employees),
                ("View All Employees Performance", library.display_all_employees_performance),
                ("Borrow Statistics", library.view_borrow_statistics),
                ("Student Statistics and Top 10 Late Students",
                 library.display_student_statistics_and_top_late),
            ])

        options.append(("Logout", self._logout_employee))
        return options

    def _logout_employee(self):
        self.current_employee = None
        self.library_system.set_current_employee(None)

    def handle_change_password(self):
        print("\n--- Change Password ---")
        current_password = input("Current password: ")
        new_password = input("New password: ")
        confirm_password = input("Confirm new password: ")

        if new_password != confirm_password:
            print("New passwords do not match.")
            return

        if self.library_system.change_employee_password(
                self.current_employee.username, current_password, new_password):
            print("Password changed successfully!")
        else:
            print("Failed to change password. Please check your current password.")

    def handle_employee_registration(self):
        print("\n--- New Employee Registration ---")
        name = input("Employee name: ")
        employee_id = input("Employee ID: ")
        username = input("Username: ")
        password = input("Password: ")
        role = input("Role (manager/staff): ")

        if role.lower() not in ("manager", "staff"):
            print("Invalid role. Please enter 'manager' or 'staff'.")
            return

        self.library_system.register_employee(name, employee_id, username, password, role.lower())

    @staticmethod
    def _print_options(options):
        for i, (label, _) in enumerate(options, start=1):
            print(f"{i}. {label}")
        print("Please enter your choice: ", end="")

    @staticmethod
    def _get_int_input(min_value, max_value):
        while True:
            try:
                value = int(input())
                if min_value <= value <= max_value:
                    return value
                print(f"Please enter a number between {min_value} and {max_value}: ", end="")
            except ValueError:
                print("Invalid input. Please enter a number: ", end="")
