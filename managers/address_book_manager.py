from datetime import datetime, timedelta
from decorators.log_decorator import log_action
from models.contact import Contact
from managers.storage_manager import StorageManager

class AddressBookManager:
    def __init__(self):
        self.storage = StorageManager("contacts.json")
        self.contacts = [Contact(**c) for c in self.storage.load()]

    @log_action
    def add_contact(self):
        name = input("Ім'я: ")
        phone = input("Телефон: ")
        email = input("Email: ")
        address = input("Адреса: ")
        birthday = input("День народження (YYYY-MM-DD): ")
        contact = Contact(name, phone, email, address, birthday)
        self.contacts.append(contact)
        self.save()
        print("✅ Контакт додано!")

    @log_action
    def add_contact_from_dict(self, data):
        new_contact = Contact(name=data["name"],
                              phone=data["phone"],
                              email=data["email"],
                              address=data["address"],
                              birthday=data["birthday"])
        self.contacts.append(new_contact)
        self.save()

    @log_action
    def list_contacts(self):
        for c in self.contacts:
            print(c)

    @log_action
    def search_contact(self):
        query = input("Введіть ім'я для пошуку: ").lower()
        results = [c for c in self.contacts if query in c.name.lower()]
        print("\n".join(map(str, results)) if results else "❌ Контакт не знайдено")

    @log_action
    def edit_contact(self):
        name = input("Ім'я контакту для редагування: ")
        for c in self.contacts:
            if c.name.lower() == name.lower():
                c.phone = input(f"Новий телефон ({c.phone}): ") or c.phone
                c.email = input(f"Новий email ({c.email}): ") or c.email
                c.address = input(f"Нова адреса ({c.address}): ") or c.address
                c.birthday = input(f"Новий день народження ({c.birthday}): ") or c.birthday
                self.save()
                print("✅ Контакт оновлено!")
                return
        print("❌ Контакт не знайдено")

    @log_action
    def delete_contact(self):
        name = input("Ім'я контакту для видалення: ")
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        self.save()
        print("✅ Контакт видалено!")

    @log_action
    def upcoming_birthdays(self):
        days = int(input("Через скільки днів показати дні народження? "))
        today = datetime.today()
        upcoming = []
        for c in self.contacts:
            bday = datetime.strptime(c.birthday, "%Y-%m-%d")
            bday_this_year = bday.replace(year=today.year)
            if today <= bday_this_year <= today + timedelta(days=days):
                upcoming.append(c)
        print("\n".join(map(str, upcoming)) if upcoming else "❌ Немає днів народження")
    
    @log_action
    def save(self):
        self.storage.save([c.__dict__ for c in self.contacts])