# Library Management System — Python Version

Python port of the Java final project in [`ap/projects/finalproject/`](../finalproject/).
Same console-based behavior, same default accounts, same `.dat` persistence files —
with `pickle` standing in for Java serialization.

## Run

Requires **Python 3.8+**. No external dependencies.

```bash
cd ap/projects/finalproject_python
python main.py
```

Default employee accounts (created automatically on first run):

| Username | Password | Role    |
|----------|----------|---------|
| `admin`  | `1234`   | manager |
| `staff`  | `1234`   | staff   |

## Structure

| Module | Java counterpart |
|--------|------------------|
| `book.py`, `student.py`, `employee.py` | `Book.java`, `Student.java`, `Employee.java` |
| `borrow_record.py`, `borrow_request.py`, `employee_performance.py` | matching `*.java` models |
| `borrow_statistics.py`, `student_statistics.py`, `student_borrow_report.py` | statistics models |
| `*_file_manager.py` | `*FileManager.java` (pickle ↔ `ObjectOutputStream`) |
| `*_manager.py` | business-logic `*Manager.java` classes |
| `library_system.py` | `LibrarySystem.java` |
| `menu_handler.py` | `MenuHandler.java` |
| `main.py` | `LibrarySystem.main()` |

Data files (`books.dat`, `students.dat`, `employees.dat`, `borrow_records.dat`,
`borrow_requests.dat`, `employee_performance.dat`) are created in the working
directory on first save, mirroring the Java version.
