"""Student domain model — Python port of ap.projects.finalproject.Student."""


class Student:
    def __init__(self, name, student_id, username, password):
        self.name = name
        self.student_id = student_id
        self.username = username
        self.password = password
        self.is_active = True

    def set_active(self, active):
        self.is_active = active

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return (f"Name: {self.name} | Student ID: {self.student_id} | "
                f"Username: {self.username} | Status: {status}")
