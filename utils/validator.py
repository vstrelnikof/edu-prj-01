import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_phone(phone: str, throw: bool = True) -> str:
        if not re.match(r"^\+380\d{9}$", phone):
            if throw:
                raise ValueError("❌ Некоректний номер телефону!")
            return ""
        return phone

    @staticmethod
    def validate_email(email: str, throw: bool = True) -> str:
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            if throw:
                raise ValueError("❌ Некоректний email!")
            return ""
        return email

    @staticmethod
    def validate_date(date_str: str, throw: bool = True) -> str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            if throw:
                raise ValueError("❌ Дата повинна бути у форматі YYYY-MM-DD")
            return ""