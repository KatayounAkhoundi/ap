"""Employee persistence — Python port of ap.projects.finalproject.EmployeeFileManager."""
import pickle

FILE_NAME = "employees.dat"


def save_employees(employees):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(employees, f)
    except OSError as e:
        print(f"Error saving employees data: {e}")


def load_employees():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return []
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading employees data: {e}")
        return []

    if isinstance(loaded, list):
        return loaded
    print("Invalid data format in employees file.")
    return []
