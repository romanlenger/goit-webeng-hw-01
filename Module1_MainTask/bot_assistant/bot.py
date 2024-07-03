from functools import wraps
from typing import Tuple, List

from bot_assistant import Record, DisplayFactory
from .data import FileProcessor
from variables import DATA


class Bot:
    def __init__(self):
        self.__data = FileProcessor(DATA)
        self.__display = DisplayFactory()

        self.book = self.__data.load_data() # returns AddressBook()
        self.messenger = self.__display.get_display('message') #returns MessageShow(), from display.py
        
    @staticmethod
    def _input_error(func):
        """
        Декоратор для обробки помилок вводу.
        """
        @wraps(func)
        def inner(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                return result
            except KeyError:
                return self.messenger.show("@input_error : KeyError : Contact not found.")
            except ValueError:
                return self.messenger.show("@input_error : ValueError : Give me name and phone please.")
            except IndexError:
                return self.messenger.show("@input_error : Index Error")
            except TypeError:
                return self.messenger.show("@input_error : TypeError")
        return inner

    @_input_error
    def add_contact(self, args):
        name, phone, *_ = args
        record = self.book.find(name)
        message = "Контакт оновлено."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Контакт додано."
        if phone:
            record.add_phone(phone)
        return message

    @_input_error
    def change_contact(self, args):
        name, old_phone, new_phone, *_ = args
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)
        self.messenger.show("Номер телефону оновлено.") 

    @_input_error
    def show_phone(self, args):
        name, *_ = args
        display = self.__display.get_display('phone')
        display.show(book=self.book, name=name)
    
    @_input_error
    def show_contact(self, args):
        name, *_ = args
        self.__display.get_display('contact').show(book=self.book, name=name)

    @_input_error
    def show_all(self):
        display = self.__display.get_display('book')
        display.show(book=self.book)

    @_input_error
    def add_birthday(self, args):
        name, birthday, *_ = args
        record = self.book.find(name)
        if record is None:
            self.messenger.show("Такого контакту не існує.")
        else:
            record.birthday = birthday
            self.messenger.show("Дата дня народження успішно додана до контакту!")

    @_input_error
    def show_birthday(self, args):
        name, *_ = args
        record = self.book.find(name)
        if record is None:
            self.messenger.show('Такого контакту не існує.')
        else:
            return record.birthday.value.date()

    @_input_error
    def birthdays(self):
        upcoming_birthdays = self.book.get_upcoming_birthdays()
        birthday_messages = [f"{birthday.name} - {birthday.date}" for birthday in upcoming_birthdays]
        self.messenger.show("\n".join(birthday_messages))

    @staticmethod
    def parse_input(user_input: str) -> Tuple[str, List[str]]:
        input_parts = user_input.strip().split()
        if not input_parts:
            return "", []  # Повертаємо порожній рядок та список, якщо ввід порожній
        command = input_parts[0].lower()
        args = input_parts[1:]
        return command, args
    
    @staticmethod
    def greeting():
        print("Вітаю, я бот-асистент!\n")
        
    def show_commands(self):
        self.__display.get_display('commands').show()

    def close(self):
        self.__data.save_data(self.book)
        self.messenger.show('Бувай здоровий!')
        
    def polling(self):
        while True:
            user_input = input("Введіть команду: ")
            command, args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                self.close()
                break

            elif command == "hello":
                print('Hello bro!')

            elif command == "help":
                self.show_commands()

            elif command == "add":
                print(self.add_contact(args))

            elif command == "change":
                print(self.change_contact(args))

            elif command == "phone":
                self.show_phone(args)

            elif command == "all":
                self.show_all()

            elif command == "show":
                self.show_contact(args)

            elif command == "add-birthday":
                self.add_birthday(args)

            elif command == "show-birthday":
                print(self.show_birthday(args))

            elif command == "birthdays":
                self.birthdays()

            else:
                print("Invalid command.")
