# Library Management System — Python Version

Python port of the Java final project in [`ap/projects/finalproject/`](../finalproject/).
Same console-based behavior, same default accounts — persisted to a **SQLite** database
by default, with the original pickle `*.dat` files still available as a secondary backend.

## Run

Requires **Python 3.8+**. No external dependencies — `sqlite3` ships with Python.

```bash
cd ap/projects/finalproject_python
python main.py
```

Default employee accounts (created automatically on first run):

| Username | Password | Role    |
|----------|----------|---------|
| `admin`  | `1234`   | manager |
| `staff`  | `1234`   | staff   |

## Storage Backends

The active backend is chosen in `storage_config.json`, created automatically on first run:

```json
{ "backend": "sqlite" }
```

| Backend | File(s) | Module |
|---------|---------|--------|
| `sqlite` (default) | `library.db` — six tables: `books`, `students`, `employees`, `borrow_records`, `borrow_requests`, `employee_performance` | `database.py` + `sqlite_storage.py` |
| `pickle` | `books.dat`, `students.dat`, `employees.dat`, `borrow_records.dat`, `borrow_requests.dat`, `employee_performance.dat` | `*_file_manager.py` |

Both backends are reached by the managers only through the `storage.py` facade, so
switching never touches business logic.

## Structure

| Module | Java counterpart |
|--------|------------------|
| `book.py`, `student.py`, `employee.py` | `Book.java`, `Student.java`, `Employee.java` |
| `borrow_record.py`, `borrow_request.py`, `employee_performance.py` | matching `*.java` models |
| `borrow_statistics.py`, `student_statistics.py`, `student_borrow_report.py` | statistics models |
| `database.py`, `sqlite_storage.py` | — (SQLite backend, new in the Python version) |
| `config.py`, `storage.py` | EX7 `Config` pattern — backend selection and dispatch |
| `*_file_manager.py` | `*FileManager.java` (pickle ↔ `ObjectOutputStream`) |
| `*_manager.py` | business-logic `*Manager.java` classes |
| `library_system.py` | `LibrarySystem.java` |
| `menu_handler.py` | `MenuHandler.java` |
| `main.py` | `LibrarySystem.main()` |

Runtime files (`library.db`, `*.dat`, `storage_config.json`) are created in the working
directory and are git-ignored.
