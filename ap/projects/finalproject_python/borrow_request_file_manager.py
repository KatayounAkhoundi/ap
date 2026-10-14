"""Borrow request persistence — Python port of ap.projects.finalproject.BorrowRequestFileManager."""
import pickle

FILE_NAME = "borrow_requests.dat"


def save_borrow_requests(requests):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(requests, f)
    except OSError as e:
        print(f"Error saving borrow requests: {e}")


def load_borrow_requests():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return []
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading borrow requests: {e}")
        return []

    if isinstance(loaded, list):
        return loaded
    print("Invalid data format in borrow requests file.")
    return []
