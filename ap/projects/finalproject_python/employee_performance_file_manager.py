"""Employee performance persistence — Python port of ap.projects.finalproject.EmployeePerformanceFileManager."""
import pickle

FILE_NAME = "employee_performance.dat"


def save_performance_records(performance_records):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(performance_records, f)
    except OSError as e:
        print(f"Error saving employee performance data: {e}")


def load_performance_records():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return {}
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading employee performance data: {e}")
        return {}

    if isinstance(loaded, dict):
        return loaded
    print("Invalid data format in employee performance file.")
    return {}
