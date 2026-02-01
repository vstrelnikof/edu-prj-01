from managers.address_book import AddressBook
from managers.notes_manager import NotesManager
from difflib import get_close_matches

class CLI:
    def __init__(self):
        self.address_book = AddressBook()
        self.notes_manager = NotesManager()

        # Єдиний словник конфігурації команд
        self.COMMANDS = {
            "add_contact": {
                "aliases": ["додати контакт", "новий контакт", "створити контакт"],
                "handler": self.address_book.add_contact,
                "description": "Додати новий контакт"
            },
            "list_contacts": {
                "aliases": ["показати контакти", "всі контакти", "список контактів"],
                "handler": self.address_book.list_contacts,
                "description": "Показати всі контакти"
            },
            "search_contact": {
                "aliases": ["знайти контакт", "пошук контакту"],
                "handler": self.address_book.search_contact,
                "description": "Пошук контакту"
            },
            "edit_contact": {
                "aliases": ["редагувати контакт", "змінити контакт"],
                "handler": self.address_book.edit_contact,
                "description": "Редагувати контакт"
            },
            "delete_contact": {
                "aliases": ["видалити контакт", "стерти контакт"],
                "handler": self.address_book.delete_contact,
                "description": "Видалити контакт"
            },
            "birthdays": {
                "aliases": ["дні народження", "показати дні народження"],
                "handler": self.address_book.upcoming_birthdays,
                "description": "Показати дні народження"
            },
            "add_note": {
                "aliases": ["додати нотатку", "нова нотатка"],
                "handler": self.notes_manager.add_note,
                "description": "Додати нову нотатку"
            },
            "list_notes": {
                "aliases": ["показати нотатки", "всі нотатки", "список нотаток"],
                "handler": self.notes_manager.list_notes,
                "description": "Показати всі нотатки"
            },
            "search_note": {
                "aliases": ["знайти нотатку", "пошук нотатки"],
                "handler": self.notes_manager.search_note,
                "description": "Пошук нотатки"
            },
            "edit_note": {
                "aliases": ["редагувати нотатку", "змінити нотатку"],
                "handler": self.notes_manager.edit_note,
                "description": "Редагувати нотатку"
            },
            "delete_note": {
                "aliases": ["видалити нотатку", "стерти нотатку"],
                "handler": self.notes_manager.delete_note,
                "description": "Видалити нотатку"
            },
            "exit": {
                "aliases": ["вихід", "завершити", "quit", "exit"],
                "handler": self._exit,
                "description": "Вихід з програми"
            }
        }

    def _exit(self):
        print("👋 До зустрічі!")
        raise SystemExit

    def _guess_command(self, user_input: str) -> str | None:
        # Вгадує найближчу команду на основі введеного тексту.
        all_keywords = {alias: cmd for cmd, cfg in self.COMMANDS.items() for alias in cfg["aliases"]}
        matches = get_close_matches(user_input.lower(), all_keywords.keys(), n=1, cutoff=0.5)
        if matches:
            return all_keywords[matches[0]]
        return None

    def _print_help(self):
        print("=== Персональний помічник ===")
        print("Доступні команди:")
        for cmd, cfg in self.COMMANDS.items():
            print(f"  {cmd:<15} – {cfg['description']}")

    def run(self):
        self._print_help()

        while True:
            command = input("\nВведіть команду: ").strip().lower()

            # Якщо команда не знайдена напряму — пробуємо вгадати
            if command not in self.COMMANDS:
                suggestion = self._guess_command(command)
                if suggestion:
                    print(f"🤔 Можливо ви мали на увазі: {suggestion}")
                    command = suggestion
                else:
                    print("❌ Невідома команда. Спробуйте ще раз.")
                    continue

            # Виконання команди через handler
            try:
                self.COMMANDS[command]["handler"]()
            except SystemExit:
                break
            except Exception as e:
                print(f"❌ Помилка: {e}")