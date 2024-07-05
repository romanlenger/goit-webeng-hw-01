from abc import ABC, abstractmethod
from typing import Literal
from functools import wraps

from bot_assistant import AddressBook
from .error_handlers import display_error
        

class Show(ABC):
    """
    Абстрактний клас для виведення даних в консоль.
    """
    def __init__(self): 
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs): 
        pass


class BookShow(Show):
    def __init__(self, book: AddressBook):
        super().__init__()
        self.book = book

    def __call__(self):
        print (' '.join(str(row) for row in self.book.data.values()))


@display_error
class PhoneShow(Show):
    def __init__(self, book: AddressBook):
        super().__init__()
        self.book = book

    def __call__(self, *args):
        name, *_ = args
        record = self.book.find(name[0])
        print ('\n'.join(ph.value for ph in record.phones))


@display_error
class RecordShow(Show):
    def __init__(self, book: AddressBook):
        super().__init__()
        self.book = book

    def __call__(self, *args):
        name, *_ = args
        record = self.book.find(name[0])
        print (f"""
            Contact name: {record.name.value},\n
            phones: {'; '.join(p.value for p in record.phones)},\n
            birthday: {record.birthday.value.date()}
        """)


class CommandsShow(Show):
    def __call__(self):
        print ("Команди:\n" + '\n'.join([
            'add [ім\'я] [номер телефону] - Створює новий контакт.',
            'del [ім\'я] - Видаляє контакт',
            'phone [ім\'я] - Виведе номер телефону вказаного контакту.', 
            'show [ім\'я] - Виводить всю інформацію по вказаному контакту.',
            'all - Виведе список усіх контактів', 
            'change [ім\'я] [старе значення] [нове значення] - Змінює номер телефону для контакту.', 
            'add-birthday [ім\'я] [DD.MM.YYYY]', 
            'show-birthday [ім\'я]', 
            'birthdays', 
            'help'
        ]))


@display_error
class MessageShow(Show):
    def __call__(self, *args):
        message, *_ = args
        print(message)
          

class Displays:
    DisplayType = Literal["book", "phone", "contact", "commands", "message"]

    def __init__(self, book: AddressBook):
        self.book = book
        self.displays = {
            "book" : BookShow(self.book),
            "phone" : PhoneShow(self.book),
            "contact" : RecordShow(self.book),
            "commands" : CommandsShow(),
            "message" : MessageShow()
        }

    def get_display(self, show_type: DisplayType) -> Show:
        return self.displays.get(show_type, None)
