"""SQLite database connection and schema for the Python port.

When the "sqlite" backend is selected (storage_config.json), this module owns
the single library.db database that replaces the pickle *.dat files.
"""
import sqlite3

DB_FILE = "library.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    isbn TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS students (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    password TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS employees (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS borrow_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_username TEXT NOT NULL,
    book_isbn TEXT NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    actual_pickup_date TEXT,
    return_date TEXT,
    is_picked_up INTEGER NOT NULL DEFAULT 0,
    is_returned INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS borrow_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_username TEXT NOT NULL,
    book_isbn TEXT NOT NULL,
    request_date TEXT NOT NULL,
    desired_borrow_date TEXT NOT NULL,
    desired_end_date TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    rejection_reason TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS employee_performance (
    employee_username TEXT PRIMARY KEY,
    books_added INTEGER NOT NULL DEFAULT 0,
    books_edited INTEGER NOT NULL DEFAULT 0,
    books_borrowed INTEGER NOT NULL DEFAULT 0,
    books_returned INTEGER NOT NULL DEFAULT 0,
    borrow_requests_approved INTEGER NOT NULL DEFAULT 0,
    borrow_requests_rejected INTEGER NOT NULL DEFAULT 0,
    last_activity_date TEXT NOT NULL
);
"""


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(_SCHEMA)
    return conn
