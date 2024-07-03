from .fields import Name, Phone, Birthday


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self._birthday = None
        self.birthday = birthday

    def add_phone(self, phone: int | float) -> None:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
                return
        raise ValueError("Номер не знайдено.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for ph in self.phones:
            if ph.value == old_phone:
                self.phones.remove(ph)
                self.phones.append(Phone(new_phone))
                return
        raise ValueError("Номер, який ви хочете змінити, не знайдено.")

    def find_phone(self, phone: str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None
    
    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = Birthday(value)

    def __str__(self):
        return f"""
        Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}
        """
    
    