"""SQLite-backed storage — mirror of the pickle *_file_manager modules.

Each save function rewrites its table from the in-memory object list; each
load function rebuilds the domain objects from rows. Dates are stored as ISO
strings and parsed back on load.
"""
from datetime import date

import database
from book import Book
from borrow_record import BorrowRecord
from borrow_request import BorrowRequest
from employee import Employee
from employee_performance import EmployeePerformance
from student import Student


def _to_date(value):
    return date.fromisoformat(value) if value else None


# ---------- Books ----------

def save_books(books):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM books")
        conn.executemany(
            "INSERT INTO books (isbn, title, author, publication_year, is_available) "
            "VALUES (?, ?, ?, ?, ?)",
            [(b.isbn, b.title, b.author, b.publication_year, 1 if b.is_available else 0)
             for b in books])
        conn.commit()
    finally:
        conn.close()


def load_books():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT isbn, title, author, publication_year, is_available FROM books").fetchall()
    finally:
        conn.close()
    books = [Book(title, author, publication_year, isbn)
             for isbn, title, author, publication_year, _ in rows]
    for book, (_, _, _, _, is_available) in zip(books, rows):
        book.is_available = bool(is_available)
    return books


# ---------- Students ----------

def save_students(students):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM students")
        conn.executemany(
            "INSERT INTO students (username, name, student_id, password, is_active) "
            "VALUES (?, ?, ?, ?, ?)",
            [(s.username, s.name, s.student_id, s.password, 1 if s.is_active else 0)
             for s in students])
        conn.commit()
    finally:
        conn.close()


def load_students():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT username, name, student_id, password, is_active FROM students").fetchall()
    finally:
        conn.close()
    students = [Student(name, student_id, username, password)
                for username, name, student_id, password, _ in rows]
    for student, (_, _, _, _, is_active) in zip(students, rows):
        student.is_active = bool(is_active)
    return students


# ---------- Employees ----------

def save_employees(employees):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM employees")
        conn.executemany(
            "INSERT INTO employees (username, name, employee_id, password, role) "
            "VALUES (?, ?, ?, ?, ?)",
            [(e.username, e.name, e.employee_id, e.password, e.role) for e in employees])
        conn.commit()
    finally:
        conn.close()


def load_employees():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT username, name, employee_id, password, role FROM employees").fetchall()
    finally:
        conn.close()
    return [Employee(name, employee_id, username, password, role)
            for username, name, employee_id, password, role in rows]


# ---------- Borrow records ----------

def save_borrow_records(records):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM borrow_records")
        conn.executemany(
            "INSERT INTO borrow_records (student_username, book_isbn, borrow_date, due_date, "
            "actual_pickup_date, return_date, is_picked_up, is_returned) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [(r.student_username, r.book_isbn, r.borrow_date.isoformat(), r.due_date.isoformat(),
              r.actual_pickup_date.isoformat() if r.actual_pickup_date else None,
              r.return_date.isoformat() if r.return_date else None,
              1 if r.is_picked_up else 0, 1 if r.is_returned else 0)
             for r in records])
        conn.commit()
    finally:
        conn.close()


def load_borrow_records():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT student_username, book_isbn, borrow_date, due_date, actual_pickup_date, "
            "return_date, is_picked_up, is_returned FROM borrow_records").fetchall()
    finally:
        conn.close()
    records = [BorrowRecord(student_username, book_isbn, _to_date(borrow_date), _to_date(due_date))
               for student_username, book_isbn, borrow_date, due_date, _, _, _, _ in rows]
    for record, (_, _, _, _, actual_pickup_date, return_date, is_picked_up, is_returned) in zip(records, rows):
        record.is_picked_up = bool(is_picked_up)
        record.is_returned = bool(is_returned)
        record.actual_pickup_date = _to_date(actual_pickup_date)
        record.return_date = _to_date(return_date)
    return records


# ---------- Borrow requests ----------

def save_borrow_requests(requests):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM borrow_requests")
        conn.executemany(
            "INSERT INTO borrow_requests (student_username, book_isbn, request_date, "
            "desired_borrow_date, desired_end_date, status, rejection_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(r.student_username, r.book_isbn, r.request_date.isoformat(),
              r.desired_borrow_date.isoformat(),
              r.desired_end_date.isoformat() if r.desired_end_date else None,
              r.status, r.rejection_reason) for r in requests])
        conn.commit()
    finally:
        conn.close()


def load_borrow_requests():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT student_username, book_isbn, request_date, desired_borrow_date, "
            "desired_end_date, status, rejection_reason FROM borrow_requests").fetchall()
    finally:
        conn.close()
    requests = [BorrowRequest(student_username, book_isbn,
                              _to_date(desired_borrow_date), _to_date(desired_end_date))
                for student_username, book_isbn, _, desired_borrow_date, desired_end_date, _, _ in rows]
    for request, (_, _, request_date, _, _, status, rejection_reason) in zip(requests, rows):
        request.request_date = _to_date(request_date)
        request.status = status
        request.rejection_reason = rejection_reason
    return requests


# ---------- Employee performance ----------

def save_performance_records(performance_records):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM employee_performance")
        conn.executemany(
            "INSERT INTO employee_performance (employee_username, books_added, books_edited, "
            "books_borrowed, books_returned, borrow_requests_approved, borrow_requests_rejected, "
            "last_activity_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [(p.employee_username, p.books_added, p.books_edited, p.books_borrowed,
              p.books_returned, p.borrow_requests_approved, p.borrow_requests_rejected,
              p.last_activity_date.isoformat()) for p in performance_records.values()])
        conn.commit()
    finally:
        conn.close()


def load_performance_records():
    conn = database.get_connection()
    try:
        rows = conn.execute(
            "SELECT employee_username, books_added, books_edited, books_borrowed, books_returned, "
            "borrow_requests_approved, borrow_requests_rejected, last_activity_date "
            "FROM employee_performance").fetchall()
    finally:
        conn.close()
    records = {}
    for (username, books_added, books_edited, books_borrowed, books_returned,
         approved, rejected, last_activity_date) in rows:
        performance = EmployeePerformance(username)
        performance.books_added = books_added
        performance.books_edited = books_edited
        performance.books_borrowed = books_borrowed
        performance.books_returned = books_returned
        performance.borrow_requests_approved = approved
        performance.borrow_requests_rejected = rejected
        performance.last_activity_date = _to_date(last_activity_date)
        records[username] = performance
    return records
