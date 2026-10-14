"""Borrow statistics — Python port of ap.projects.finalproject.BorrowStatistics."""


class BorrowStatistics:
    def __init__(self, borrow_records, borrow_requests):
        self._calculate_statistics(borrow_records, borrow_requests)

    def _calculate_statistics(self, borrow_records, borrow_requests):
        self.total_borrow_requests = len(borrow_requests)
        self.approved_borrow_requests = sum(1 for r in borrow_requests if r.is_approved())
        self.rejected_borrow_requests = sum(1 for r in borrow_requests if r.is_rejected())
        self.pending_borrow_requests = sum(1 for r in borrow_requests if r.is_pending())

        self.total_borrows = len(borrow_records)
        self.active_borrows = sum(1 for r in borrow_records if not r.is_returned and r.is_picked_up)
        self.completed_borrows = sum(1 for r in borrow_records if r.is_returned)
        self.overdue_borrows = sum(1 for r in borrow_records if r.is_overdue())

        self._calculate_average_borrow_days(borrow_records)

    def _calculate_average_borrow_days(self, borrow_records):
        total_days = 0
        count = 0

        for record in borrow_records:
            if record.is_returned and record.actual_pickup_date is not None and record.return_date is not None:
                total_days += (record.return_date - record.actual_pickup_date).days
                count += 1

        self.average_borrow_days = total_days / count if count > 0 else 0.0

    def display_statistics(self):
        print("\n=== Borrow Statistics ===")
        print("=== Borrow Requests ===")
        print(f"Total Borrow Requests: {self.total_borrow_requests}")
        print(f"Approved Requests: {self.approved_borrow_requests}")
        print(f"Rejected Requests: {self.rejected_borrow_requests}")
        print(f"Pending Requests: {self.pending_borrow_requests}")

        print("\n=== Borrow Operations ===")
        print(f"Total Borrows: {self.total_borrows}")
        print(f"Active Borrows: {self.active_borrows}")
        print(f"Completed Borrows: {self.completed_borrows}")
        print(f"Overdue Borrows: {self.overdue_borrows}")
        print(f"Average Borrow Duration: {self.average_borrow_days:.2f} days")

        if self.total_borrow_requests > 0:
            approval_rate = (self.approved_borrow_requests * 100.0) / self.total_borrow_requests
            rejection_rate = (self.rejected_borrow_requests * 100.0) / self.total_borrow_requests
            print(f"\nApproval Rate: {approval_rate:.1f}%")
            print(f"Rejection Rate: {rejection_rate:.1f}%")

        if self.total_borrows > 0:
            completion_rate = (self.completed_borrows * 100.0) / self.total_borrows
            overdue_rate = (self.overdue_borrows * 100.0) / self.total_borrows
            print(f"Completion Rate: {completion_rate:.1f}%")
            print(f"Overdue Rate: {overdue_rate:.1f}%")
