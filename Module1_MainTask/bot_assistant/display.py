from abc import ABC, abstractmethod

from bot_assistant import AddressBook   


class Show(ABC):
    """
    Абстрактний клас для виведення даних в консоль.
    """
    @abstractmethod
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        pass


class BookShow(Show):
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        print (' '.join(str(row) for row in book.data.values()))


class PhoneShow(Show):
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        record = book.find(name)
        print ('\n'.join(ph.value for ph in record.phones))


class RecordShow(Show):
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        record = book.find(name)
        print (f"""
        Contact name: {record.name.value},\n
        phones: {'; '.join(p.value for p in record.phones)},\n
        birthday: {record.birthday.value.date()}
        """)


class CommandsShow(Show):
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        print ("Команди:\n" + '\n'.join([
            'add [ім\'я] [номер телефону] - Створює новий контакт.', 
            'phone [ім\'я] - Виведе номер телефону вказаного контакту.', 
            'show [ім\'я] - Виводить всю інформацію по вказаному контакту.',
            'all - Виведе список усіх контактів', 
            'change [ім\'я] [старе значення] [нове значення] - Змінює номер телефону для контакту.', 
            'add-birthday [ім\'я] [DD.MM.YYYY]', 
            'show-birthday [ім\'я]', 
            'birthdays', 
            'help'
            ]))
    

class MessageShow(Show):
    def show(self, message: str = None, book: AddressBook = None, name: str = None):
        print(message)


class DisplayFactory:
    def __init__(self):
        self.displays = {
            "book" : BookShow(),
            "phone" : PhoneShow(),
            "contact" : RecordShow(),
            "commands" : CommandsShow(),
            "message" : MessageShow()
        }

    def get_display(self, show_type: str) -> Show:
        return self.displays.get(show_type, None)
