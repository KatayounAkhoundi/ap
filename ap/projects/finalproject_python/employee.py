"""Employee domain model — Python port of ap.projects.finalproject.Employee."""


class Employee:
    def __init__(self, name, employee_id, username, password, role):
        self.name = name
        self.employee_id = employee_id
        self.username = username
        self.password = password
        self.role = role

    def is_manager(self):
        return self.role.lower() == "manager"

    def is_staff(self):
        return self.role.lower() == "staff"

    def __str__(self):
        return (f"Name: {self.name} | Employee ID: {self.employee_id} | "
                f"Username: {self.username} | Role: {self.role}")
