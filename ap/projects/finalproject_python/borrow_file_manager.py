"""Borrow record persistence — Python port of ap.projects.finalproject.BorrowFileManager."""
import pickle

FILE_NAME = "borrow_records.dat"


def save_borrow_records(records):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(records, f)
    except OSError as e:
        print(f"Error saving borrow records: {e}")


def load_borrow_records():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return []
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading borrow records: {e}")
        return []

    if isinstance(loaded, list):
        return loaded
    print("Invalid data format in borrow records file.")
    return []
