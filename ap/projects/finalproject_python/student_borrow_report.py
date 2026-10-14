"""Student borrow report — Python port of ap.projects.finalproject.StudentBorrowReport."""


class StudentBorrowReport:
    def __init__(self, student_username, borrow_history):
        self.student_username = student_username
        self.borrow_history = borrow_history
        self.total_borrows = len(borrow_history)
        self.not_delivered_count = sum(
            1 for r in borrow_history if not r.is_picked_up and not r.is_returned)
        self.active_borrows = sum(
            1 for r in borrow_history if r.is_picked_up and not r.is_returned)
        self.currently_overdue_count = sum(1 for r in borrow_history if r.is_overdue())
        self.late_return_count = sum(1 for r in borrow_history if r.is_returned_late())
        self.returned_borrows = sum(1 for r in borrow_history if r.is_returned)

    def display_report(self):
        print("\n=== Student Borrow Report ===")
        print(f"Student Username: {self.student_username}")
        print(f"Total Borrows: {self.total_borrows}")
        print(f"Not Delivered Yet (Ready for Pickup): {self.not_delivered_count}")
        print(f"Active Borrows: {self.active_borrows}")
        print(f"Currently Overdue: {self.currently_overdue_count}")
        print(f"Returned Late: {self.late_return_count}")
        print(f"Returned: {self.returned_borrows}")

        print("\n--- Borrow History ---")
        if not self.borrow_history:
            print("No borrow history found.")
        else:
            for record in self.borrow_history:
                print(record)

        return_rate = (self.returned_borrows * 100.0 / self.total_borrows) if self.total_borrows > 0 else 0
        print(f"\nReturn Rate: {return_rate:.1f}%")

        if self.currently_overdue_count > 0:
            print(f"This student has {self.currently_overdue_count} currently overdue book(s)!")
        if self.late_return_count > 0:
            print(f"This student has returned {self.late_return_count} book(s) late!")
