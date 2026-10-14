"""Book persistence — Python port of ap.projects.finalproject.BookFileManager.

Java serializes to books.dat with ObjectOutputStream; here pickle plays the
same role and the file name is kept for parity.
"""
import pickle

FILE_NAME = "books.dat"


def save_books(books):
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump(books, f)
    except OSError as e:
        print(f"Error saving books data: {e}")


def load_books():
    try:
        with open(FILE_NAME, "rb") as f:
            loaded = pickle.load(f)
    except FileNotFoundError:
        return None
    except (OSError, pickle.UnpicklingError) as e:
        print(f"Error loading books data: {e}")
        return []

    if isinstance(loaded, list):
        return loaded
    print("Invalid data format in file.")
    return []
