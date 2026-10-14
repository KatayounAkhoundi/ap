"""Student business logic — Python port of ap.projects.finalproject.StudentManager."""
import student_file_manager
from student_statistics import StudentStatistics


class StudentManager:
    def __init__(self):
        self.students = student_file_manager.load_students()
        if self.students is None:
            self.students = []

    def generate_student_statistics(self, borrow_records):
        return StudentStatistics(self.students, borrow_records)

    def display_students_with_most_late(self, limit, borrow_records):
        late_infos = []
        for student in self.students:
            late_count = sum(
                1 for record in borrow_records
                if record.student_username == student.username and record.is_late())
            if late_count > 0:
                late_infos.append((student, late_count))

        late_infos.sort(key=lambda info: info[1], reverse=True)
        top_late_students = late_infos[:limit]

        print(f"\n=== Top {limit} Students with Most Late Books ===")
        if not top_late_students:
            print("No students with late books.")
            return

        for i, (student, late_count) in enumerate(top_late_students, start=1):
            print(f"{i}. {student.name} ({student.username}) - {late_count} late book(s)")

    def register_student(self, name, student_id, username, password):
        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if self._is_username_taken(username):
            print("This username already exists. Please choose a different username.")
            return

        from student import Student
        self.students.append(Student(name, student_id, username, password))
        student_file_manager.save_students(self.students)
        print("Student registration completed successfully.")

    def authenticate_student(self, username, password):
        student = None
        for s in self.students:
            if s.username == username and s.password == password:
                student = s
                break

        if student is not None and not student.is_active:
            print("Your account is inactive. Please contact the library administrator.")
            return None

        return student

    def update_student_info(self, username, new_name, new_password):
        student = self.find_student_by_username(username)
        if student is None:
            return False

        updated = False
        if new_name:
            student.name = new_name
            updated = True
        if new_password:
            student.password = new_password
            updated = True
        if updated:
            student_file_manager.save_students(self.students)
        return updated

    def toggle_student_status(self, username):
        student = self.find_student_by_username(username)
        if student is not None:
            student.set_active(not student.is_active)
            student_file_manager.save_students(self.students)
            return True
        return False

    def find_student_by_username(self, username):
        for s in self.students:
            if s.username == username:
                return s
        return None

    def _is_username_taken(self, username):
        return any(s.username == username for s in self.students)

    def get_student_count(self):
        return len(self.students)
