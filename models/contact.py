from dataclasses import dataclass
from datetime import date, datetime
from helpers.date_helpers import replace_date_year
from models.base_model import BaseModel
from utils.validator import Validator

@dataclass
class Contact(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    birthday: str

    @property
    def birthday_date(self) -> (date | None):
        if not self.birthday:
            return None
        contact_birthday: datetime = datetime.strptime(self.birthday, "%Y-%m-%d")
        return contact_birthday.date()

    def validate(self) -> dict:
        return {
            "name": not self.name,
            "phone": not self.phone or Validator.validate_phone(self.phone),
            "email": not self.email or Validator.validate_email(self.email),
            "birthday": not self.birthday or Validator.validate_date(self.birthday)
        }
    
    def get_next_birthday_date(self, today: datetime | date = datetime.now().date()) -> (date | None):
        contact_birthday: date | None = self.birthday_date
        if not contact_birthday:
            return None
        this_year_birthday = replace_date_year(contact_birthday, today.year)
        next_birthday = replace_date_year(this_year_birthday, today.year + 1) \
            if this_year_birthday < today else this_year_birthday
        return next_birthday

    def __str__(self):
        return f"{self.name.ljust(15)} | 📱 {self.phone} | 🎂 {self.birthday}"
