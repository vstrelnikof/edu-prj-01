from dataclasses import dataclass
from models.base_model import BaseModel
from utils.validator import Validator

@dataclass
class Contact(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    birthday: str

    def validate(self):
        # Присвоєння результату валідації для очищення даних
        self.phone = Validator.validate_phone(self.phone)
        self.email = Validator.validate_email(self.email)
        self.birthday = Validator.validate_date(self.birthday)

    def __str__(self):
        return f"{self.name.ljust(15)} | 📱 {self.phone} | 🎂 {self.birthday}"
