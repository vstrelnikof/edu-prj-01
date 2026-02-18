from typing import Any
from managers.address_book_manager import AddressBookManager
from managers.notes_manager import NotesManager

class Commands(dict):
    def __init__(self, *args, **kwargs):
        address_book_manager = AddressBookManager()
        notes_manager = NotesManager()

        super().__init__({
            "add_contact": {
                "aliases": ["додати контакт", "новий контакт", "створити контакт"],
                "handler": address_book_manager.add_contact,
                "description": "Додати новий контакт"
            },
            "list_contacts": {
                "aliases": ["показати контакти", "всі контакти", "список контактів"],
                "handler": address_book_manager.list_contacts,
                "description": "Показати всі контакти"
            },
            "search_contact": {
                "aliases": ["знайти контакт", "пошук контакту"],
                "handler": address_book_manager.search_contact,
                "description": "Пошук контакту"
            },
            "edit_contact": {
                "aliases": ["редагувати контакт", "змінити контакт"],
                "handler": address_book_manager.edit_contact,
                "description": "Редагувати контакт"
            },
            "delete_contact": {
                "aliases": ["видалити контакт", "стерти контакт"],
                "handler": address_book_manager.delete_contact,
                "description": "Видалити контакт"
            },
            "birthdays": {
                "aliases": ["дні народження", "показати дні народження"],
                "handler": address_book_manager.upcoming_birthdays,
                "description": "Показати дні народження"
            },
            "add_note": {
                "aliases": ["додати нотатку", "нова нотатка"],
                "handler": notes_manager.add_note,
                "description": "Додати нову нотатку"
            },
            "list_notes": {
                "aliases": ["показати нотатки", "всі нотатки", "список нотаток"],
                "handler": notes_manager.list_notes,
                "description": "Показати всі нотатки"
            },
            "search_note": {
                "aliases": ["знайти нотатку", "пошук нотатки"],
                "handler": notes_manager.search_note,
                "description": "Пошук нотатки"
            },
            "edit_note": {
                "aliases": ["редагувати нотатку", "змінити нотатку"],
                "handler": notes_manager.edit_note,
                "description": "Редагувати нотатку"
            },
            "delete_note": {
                "aliases": ["видалити нотатку", "стерти нотатку"],
                "handler": notes_manager.delete_note,
                "description": "Видалити нотатку"
            },
            "exit": {
                "aliases": ["вихід", "завершити", "quit", "exit"],
                "handler": self._exit,
                "description": "Вихід з програми"
            }
        })
        
        self.update(*args, **kwargs)

    def _exit(self):
        print("👋 До зустрічі!")
        raise SystemExit

