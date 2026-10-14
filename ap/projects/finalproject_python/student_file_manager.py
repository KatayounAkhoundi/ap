"""Student persistence — Python port of ap.projects.finalproject.StudentFileManager."""
import pickle

FILE_NAME = "students.dat"


def save_students(students):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(students, f)
    except OSError as e:
        print(f"Error saving students data: {e}")


def load_students():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return []
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading students data: {e}")
        return []

    if isinstance(loaded, list):
        return loaded
    print("Invalid data format in file. Starting with empty list.")
    return []
