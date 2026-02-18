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

    def validate(self) -> dict:
        return {
            "phone": Validator.validate_phone(self.phone),
            "email": Validator.validate_email(self.email),
            "birthday": Validator.validate_date(self.birthday)
        }

    def __str__(self):
        return f"{self.name.ljust(15)} | 📱 {self.phone} | 🎂 {self.birthday}"
