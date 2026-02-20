from models.app_config import AppConfig
from services.address_book_service import AddressBookService
from services.notes_service import NotesService

class AppState:
    """Об'єкт стану, що зберігає всі менеджери та глобальні налаштування."""
    edit_index: int | None = None

    def __init__(self, app_config: AppConfig | None) -> None:
        self.tui_theme = app_config.theme if app_config else "bright"
        self.address_book_manager = AddressBookService()
        self.notes_manager = NotesService()

    def get_stats(self) -> dict[str, int]:
        return {
            "contacts": len(self.address_book_manager.contacts),
            "notes": len(self.notes_manager.notes)
        }
