from collections import namedtuple
from datetime import date, datetime
from decorators.log_decorator import log_action
from models.contact import Contact
from providers.storage_provider import StorageProvider
from services.base_service import BaseService

class AddressBookService(BaseService):
    contacts: list[Contact]

    def __init__(self) -> None:
        self._reload()

    def find_contact_by_id(self, id: str) -> (Contact | None):
        return next((contact for contact in self.contacts if contact.id == id), None)

    @log_action
    def add_contact(self, data: dict) -> None:
        new_contact: Contact = self.__get_contact_from_dict(data)
        if not new_contact.is_valid():
            return
        self.contacts.append(new_contact)
        self.save()
    
    @log_action
    def edit_contact(self, index: int, data: dict) -> None:
        updated_contact: Contact = self.__get_contact_from_dict(data)
        if not updated_contact.is_valid():
            return
        self.contacts[index] = updated_contact
        self.save()

    @log_action
    def delete_contact(self, index: int) -> None:
        self.contacts.pop(index)
        self.save()
    
    def get_contacts_table_data(self, search_term: str) -> list:
        table_data: list = []
        for i, contact in enumerate(self.contacts):
            is_relevant: bool = any([contact for _, contact_field_value in vars(contact).items()
                                     if search_term in contact_field_value.lower()])
            if not is_relevant:
                continue
            birthday_date: date | None = contact.birthday_date
            birthday = birthday_date.isoformat() if birthday_date else ""
            table_data.append(([contact.name,
                                contact.phone,
                                contact.email,
                                contact.address,
                                birthday], i))
        return table_data
    
    def get_birthdays_table_data(self, days: int) -> list:
        table_data: list = []
        today: date = datetime.now().date()
        for i, contact in enumerate(self.contacts):
            birthday_date: date | None = contact.get_next_birthday_date(today)
            if not birthday_date or not self.is_birthday_soon(birthday_date, days, today):
                continue
            table_data.append(([birthday_date.isoformat(),
                                contact.phone,
                                contact.email,
                                contact.address,
                                contact.name], i))
        table_data.sort(key=lambda table_row: table_row[0][0])
        return table_data

    def get_dashboard_birthdays(self) -> list[str]:
        ContactBirthday = namedtuple('ContactBirthday', ['birthday_date', 'contact'])
        upcoming_contacts: list[ContactBirthday] = []
        for contact in self.contacts:
            next_birthday_date: date | None = contact.get_next_birthday_date()
            if next_birthday_date and self.is_birthday_soon(next_birthday_date, 7):
                upcoming_contacts.append(ContactBirthday(next_birthday_date, contact))
        upcoming_contacts.sort(key=lambda row: row.birthday_date)
        return list(map(lambda row: f"  • {row.birthday_date.strftime('%d.%m')}: {row.contact.name}", upcoming_contacts)) \
            if upcoming_contacts else ["На найближчий тиждень іменинників немає"]
    
    def is_birthday_soon(self, next_birthday_date: date, days: int, today: datetime | date = datetime.now().date()) -> bool:
        # Рахуємо різницю в днях
        days_until: int = (next_birthday_date - today).days
        return 0 <= days_until <= days
    
    @log_action
    def save(self) -> None:
        self.storage.save([c.__dict__ for c in self.contacts])

    @log_action
    def _reload(self) -> None:
        self.storage = StorageProvider("contacts.json")
        self.contacts = [Contact(**c) for c in self.storage.load()]
    
    def __get_contact_from_dict(self, data: dict) -> Contact:
        birthday = data["birthday"]
        birthday = datetime.strptime(birthday, "%Y-%m-%d").date().isoformat() \
            if birthday else birthday
        return Contact(name=data["name"],
                       phone=data["phone"],
                       email=data["email"],
                       address=data["address"],
                       birthday=birthday)