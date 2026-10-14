"""Storage facade — every manager talks to the active backend through this.

Picks between the SQLite backend (sqlite_storage + database.py) and the
pickle backend (*_file_manager modules) based on config.py.
"""
import book_file_manager as _books_pickle
import borrow_file_manager as _borrows_pickle
import borrow_request_file_manager as _requests_pickle
import config
import employee_file_manager as _employees_pickle
import employee_performance_file_manager as _performance_pickle
import sqlite_storage
import student_file_manager as _students_pickle


def _use_sqlite():
    return config.get_storage_backend() == "sqlite"


# ---------- Books ----------

def save_books(books):
    if _use_sqlite():
        sqlite_storage.save_books(books)
    else:
        _books_pickle.save_books(books)


def load_books():
    if _use_sqlite():
        return sqlite_storage.load_books()
    return _books_pickle.load_books()


# ---------- Students ----------

def save_students(students):
    if _use_sqlite():
        sqlite_storage.save_students(students)
    else:
        _students_pickle.save_students(students)


def load_students():
    if _use_sqlite():
        return sqlite_storage.load_students()
    return _students_pickle.load_students()


# ---------- Employees ----------

def save_employees(employees):
    if _use_sqlite():
        sqlite_storage.save_employees(employees)
    else:
        _employees_pickle.save_employees(employees)


def load_employees():
    if _use_sqlite():
        return sqlite_storage.load_employees()
    return _employees_pickle.load_employees()


# ---------- Borrow records ----------

def save_borrow_records(records):
    if _use_sqlite():
        sqlite_storage.save_borrow_records(records)
    else:
        _borrows_pickle.save_borrow_records(records)


def load_borrow_records():
    if _use_sqlite():
        return sqlite_storage.load_borrow_records()
    return _borrows_pickle.load_borrow_records()


# ---------- Borrow requests ----------

def save_borrow_requests(requests):
    if _use_sqlite():
        sqlite_storage.save_borrow_requests(requests)
    else:
        _requests_pickle.save_borrow_requests(requests)


def load_borrow_requests():
    if _use_sqlite():
        return sqlite_storage.load_borrow_requests()
    return _requests_pickle.load_borrow_requests()


# ---------- Employee performance ----------

def save_performance_records(performance_records):
    if _use_sqlite():
        sqlite_storage.save_performance_records(performance_records)
    else:
        _performance_pickle.save_performance_records(performance_records)


def load_performance_records():
    if _use_sqlite():
        return sqlite_storage.load_performance_records()
    return _performance_pickle.load_performance_records()
