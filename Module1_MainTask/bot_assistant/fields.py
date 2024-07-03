from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.__validate_phone(value):
            raise ValueError("Телефон повинен містити 10 цифр!")
        super().__init__(value)

    @staticmethod
    def __validate_phone(phone) -> bool:
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        except TypeError:
            self.value = None
