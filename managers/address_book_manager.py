from datetime import datetime, timedelta
from decorators.log_decorator import log_action
from models.contact import Contact
from managers.storage_manager import StorageManager

class AddressBookManager:
    def __init__(self):
        self._reload()

    def find_contact_by_id(self, id: str) -> (Contact | None):
        return next((contact for contact in self.contacts if contact.id == id), None)

    @log_action
    def add_contact(self, data: dict) -> None:
        new_contact = Contact(name=data["name"],
                              phone=data["phone"],
                              email=data["email"],
                              address=data["address"],
                              birthday=data["birthday"])
        self.contacts.append(new_contact)
        self.save()
    
    @log_action
    def edit_contact(self, index: int, data: dict) -> None:
        self.contacts[index] = Contact(name=data["name"],
                                       phone=data["phone"],
                                       email=data["email"],
                                       address=data["address"],
                                       birthday=data["birthday"])
        self.save()

    @log_action
    def delete_contact(self, index: int) -> None:
        self.contacts.pop(index)
        self.save()

    @log_action
    def get_upcoming_birthdays(self, days: int = 7) -> list[str]:
        today: datetime = datetime.today()
        upcoming: list = []
        for c in self.contacts:
            bday: datetime = datetime.strptime(c.birthday, "%Y-%m-%d")
            bday_this_year: datetime = bday.replace(year=today.year)
            if today <= bday_this_year <= today + timedelta(days=days):
                upcoming.append(f"{c.name} ({bday_this_year.strftime('%d.%m')})")
        return upcoming if upcoming else ["На найближчий тиждень іменинників немає"]
    
    @log_action
    def save(self):
        self.storage.save([c.__dict__ for c in self.contacts])

    @log_action
    def _reload(self):
        self.storage = StorageManager("contacts.json")
        self.contacts = [Contact(**c) for c in self.storage.load()]