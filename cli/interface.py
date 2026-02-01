from managers.address_book import AddressBook
from managers.notes_manager import NotesManager
from difflib import get_close_matches

# Словник команд та їхніх псевдонімів
COMMAND_ALIASES = {
    "add_contact": ["додати контакт", "новий контакт", "створити контакт"],
    "list_contacts": ["показати контакти", "всі контакти", "список контактів"],
    "search_contact": ["знайти контакт", "пошук контакту"],
    "edit_contact": ["редагувати контакт", "змінити контакт"],
    "delete_contact": ["видалити контакт", "стерти контакт"],
    "birthdays": ["дні народження", "показати дні народження"],
    "add_note": ["додати нотатку", "нова нотатка"],
    "list_notes": ["показати нотатки", "всі нотатки", "список нотаток"],
    "search_note": ["знайти нотатку", "пошук нотатки"],
    "edit_note": ["редагувати нотатку", "змінити нотатку"],
    "delete_note": ["видалити нотатку", "стерти нотатку"],
    "exit": ["вихід", "завершити", "quit", "exit"]
}

def guess_command(user_input: str) -> str | None:
    # Вгадує найближчу команду на основі введеного тексту.
    all_keywords = {alias: cmd for cmd, aliases in COMMAND_ALIASES.items() for alias in aliases}
    matches = get_close_matches(user_input.lower(), all_keywords.keys(), n=1, cutoff=0.5)
    if matches:
        return all_keywords[matches[0]]
    return None


class CLI:
    def __init__(self):
        self.address_book = AddressBook()
        self.notes_manager = NotesManager()

    def run(self):
        print("=== Персональний помічник ===")
        print("Команди: add_contact, list_contacts, search_contact, edit_contact, delete_contact, birthdays, add_note, list_notes, search_note, edit_note, delete_note, exit")

        while True:
            command = input("\nВведіть команду: ").strip().lower()

            # Якщо користувач ввів псевдонім або довільний текст
            if command not in COMMAND_ALIASES.keys():
                suggestion = guess_command(command)
                if suggestion:
                    print(f"🤔 Можливо ви мали на увазі: {suggestion}")
                    command = suggestion
                else:
                    print("❌ Невідома команда. Спробуйте ще раз.")
                    continue

            # Виконання команд через match-case
            match command:
                case "add_contact": self.address_book.add_contact()
                case "list_contacts": self.address_book.list_contacts()
                case "search_contact": self.address_book.search_contact()
                case "edit_contact": self.address_book.edit_contact()
                case "delete_contact": self.address_book.delete_contact()
                case "birthdays": self.address_book.upcoming_birthdays()
                case "add_note": self.notes_manager.add_note()
                case "list_notes": self.notes_manager.list_notes()
                case "search_note": self.notes_manager.search_note()
                case "edit_note": self.notes_manager.edit_note()
                case "delete_note": self.notes_manager.delete_note()
                case "exit":
                    print("👋 До зустрічі!")
                    break
                case _: print("❌ Невідома команда")