from managers.address_book_manager import AddressBookManager
from managers.notes_manager import NotesManager

class AppState:
    edit_index: (int | None) = None

    """Об'єкт стану, що зберігає всі менеджери та глобальні налаштування."""
    def __init__(self) -> None:
        self.tui_theme = "bright" # default/monochrome/green/bright
        self.address_book_manager = AddressBookManager()
        self.notes_manager = NotesManager()

    def get_stats(self) -> dict[str, int]:
        return {
            "contacts": len(self.address_book_manager.contacts),
            "notes": len(self.notes_manager.notes)
        }
