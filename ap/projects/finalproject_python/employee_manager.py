"""Employee business logic — Python port of ap.projects.finalproject.EmployeeManager."""
import storage
from employee import Employee


class EmployeeManager:
    def __init__(self):
        self.employees = storage.load_employees()
        if not self.employees:
            self.employees = []
            self._initialize_default_employees()

    def _initialize_default_employees(self):
        self.employees.append(Employee("mr.shahi", "1111", "admin", "1234", "manager"))
        self.employees.append(Employee("mrs.tiem", "2222", "staff", "1234", "staff"))
        self._save_employees()

    def register_employee(self, name, employee_id, username, password, role):
        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if self._is_username_taken(username):
            print("This username already exists. Please choose a different username.")
            return

        self.employees.append(Employee(name, employee_id, username, password, role))
        self._save_employees()
        print("Employee registration completed successfully.")

    def authenticate_employee(self, username, password):
        for e in self.employees:
            if e.username == username and e.password == password:
                return e
        return None

    def change_password(self, username, current_password, new_password):
        employee = self._find_employee_by_username(username)
        if employee is not None and employee.password == current_password:
            employee.password = new_password
            self._save_employees()
            return True
        return False

    def _find_employee_by_username(self, username):
        for e in self.employees:
            if e.username == username:
                return e
        return None

    def _is_username_taken(self, username):
        return any(e.username == username for e in self.employees)

    def display_all_employees(self):
        print("\n--- List of Employees ---")
        if not self.employees:
            print("No employees registered yet.")
            return

        for employee in self.employees:
            print(employee)

    def _save_employees(self):
        storage.save_employees(self.employees)
