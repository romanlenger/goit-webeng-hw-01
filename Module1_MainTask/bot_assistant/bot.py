from typing import Tuple, List

from bot_assistant import Record, Displays
from .error_handlers import bot_error
from .data import FileProcessor
from variables import DATA


class Bot:
    def __init__(self):
        self.__data = FileProcessor(DATA)
        self.book = self.__data.load_data() # returns AddressBook()

        self.__displays = Displays(self.book)

        self.message = self.__displays.get_display('message') #returns MessageShow object
        self.show_phone = self.__displays.get_display('phone')
        self.show_book = self.__displays.get_display('book')
        self.show_commands = self.__displays.get_display('commands')
        self.show_contact = self.__displays.get_display('contact')
        
    @bot_error
    def add_contact(self, args):
        name, phone, *_ = args
        record = self.book.find(name)
        self.message("Контакт оновлено.")
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            self.message("Контакт додано.")
        if phone:
            record.add_phone(phone)

    @bot_error
    def delete_contact(self, args):
        name, *_ = args
        self.book.delete(name)
        self.message('Контакт видалено!')

    @bot_error
    def change_contact(self, args):
        name, old_phone, new_phone, *_ = args
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)
        self.message("Номер телефону оновлено.") 
    
    @bot_error
    def add_birthday(self, args):
        name, birthday, *_ = args
        record = self.book.find(name)
        if record is None:
            self.message("Такого контакту не існує.")
        else:
            record.birthday = birthday
            self.message("Дата дня народження успішно додана до контакту!")

    @bot_error
    def show_birthday(self, args):
        name, *_ = args
        record = self.book.find(name)
        message = record.birthday.value.date()
        self.message(message)

    @staticmethod
    def parse_input(user_input: str) -> Tuple[str, List[str]]:
        input_parts = user_input.strip().split()
        if not input_parts:
            return "", []  # Повертаємо порожній рядок та список, якщо ввід порожній
        command = input_parts[0].lower()
        args = input_parts[1:]
        return command, args

    def polling(self):
        self.message('Вітаю, я бот-асистент\n')
        self.show_commands()
        
        while True:
            user_input = input("Введіть команду: ")
            command, args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                self.__data.save_data(self.book)
                self.message('Бувай здоровий!')
                break

            elif command == "hello":
                self.message('Hello bro!')

            elif command == "help":
                self.show_commands()

            elif command == "add":
                self.add_contact(args)
            
            elif command == 'del':
                self.delete_contact(args)

            elif command == "change":
                self.change_contact(args)

            elif command == "phone":
                self.show_phone(args)

            elif command == "all":
                self.show_book()

            elif command == "show":
                self.show_contact(args)

            elif command == "add-birthday":
                self.add_birthday(args)

            elif command == "show-birthday":
                self.show_birthday(args)

            elif command == "birthdays":
                self.message(self.book.get_upcoming_birthdays())

            else:
                self.message("Invalid command.")
