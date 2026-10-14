"""Student statistics — Python port of ap.projects.finalproject.StudentStatistics."""


class StudentStatistics:
    def __init__(self, students, borrow_records):
        self._calculate_statistics(students, borrow_records)

    def _calculate_statistics(self, students, borrow_records):
        self.total_students = len(students)
        self.active_students = sum(1 for s in students if s.is_active)
        self.inactive_students = self.total_students - self.active_students

        self.total_borrows = len(borrow_records)
        self.undelivered_borrows = sum(1 for r in borrow_records if not r.is_picked_up and not r.is_returned)
        self.late_borrows = sum(1 for r in borrow_records if r.is_late())

        self.students_with_borrows = sum(1 for s in students if self._has_borrows(s.username, borrow_records))
        self.students_with_late_books = sum(
            1 for s in students if self._has_late_borrows(s.username, borrow_records))

        self.average_borrows_per_student = (
            self.total_borrows / self.students_with_borrows if self.students_with_borrows > 0 else 0)

    @staticmethod
    def _has_borrows(username, borrow_records):
        return any(r.student_username == username for r in borrow_records)

    @staticmethod
    def _has_late_borrows(username, borrow_records):
        return any(r.student_username == username and r.is_late() for r in borrow_records)

    def display_statistics(self):
        print("\n=== Student Statistics ===")
        print(f"Total Students: {self.total_students}")
        print(f"Active Students: {self.active_students}")
        print(f"Inactive Students: {self.inactive_students}")

        print("\n--- Borrow Statistics (All Students) ---")
        print(f"Total Borrows: {self.total_borrows}")
        print(f"Undelivered Books (Ready for Pickup): {self.undelivered_borrows}")
        print(f"Late Borrows: {self.late_borrows}")
        print(f"Students with Borrows: {self.students_with_borrows}")
        print(f"Students with Late Books: {self.students_with_late_books}")
        print(f"Average Borrows per Student: {self.average_borrows_per_student:.2f}")
