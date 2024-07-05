from datetime import date
from collections import UserDict
from typing import List, Dict
from datetime import timedelta

from .record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name, None)
    
    def delete(self, name: str) -> None | str:
        if name in self.data:
            del self.data[name]
        else:
            return "record not found."
    
    @staticmethod
    def _date_to_string(date: date) -> str:
        return date.strftime("%Y.%m.%d")
    
    @staticmethod
    def _find_next_weekday(start_date: date, weekday: int) -> date:
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)    

    def _adjust_for_weekend(self, birthday) -> date:
        if birthday.weekday() >= 5:
            return self._find_next_weekday(birthday, 0)
        return birthday
        
    def get_upcoming_birthdays(self) -> List[Dict]:
        upcoming_birthdays = []
        today = date.today()
        for rec in self.data.values():
            if rec.birthday.value is None:
                continue
            birthday_this_year = rec.birthday.value.replace(year=today.year).date()

            # Перевірка, чи не буде припадати день народження вже наступного року
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Перенесення дати привітання на наступний робочий день, якщо день народження припадає на вихідний
            birthday_this_year = self._adjust_for_weekend(birthday_this_year)
            
            # Перевірка, чи день народження випадає протягом наступних 7 днів
            if 0 <= (birthday_this_year - today).days <= 7:
                congratulation_date_str = self._date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": rec.name.value, "congratulation_date": congratulation_date_str})

        return upcoming_birthdays
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    


