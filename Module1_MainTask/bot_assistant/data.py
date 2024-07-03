import pickle
from bot_assistant import AddressBook


class FileProcessor():
    def __init__(self, filename: str):
        self.filename = filename

    def save_data(self, book: AddressBook):
        with open(self.filename, "wb") as f:
            pickle.dump(book, f)        

    def load_data(self):
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()

