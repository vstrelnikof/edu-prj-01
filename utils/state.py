from typing import final

from models.app_config import AppConfig
from providers.storage_provider import StorageProvider
from services.address_book_service import AddressBookService
from services.notes_service import NotesService

@final
class AppState:
    """Об'єкт стану, що зберігає екземпляри сервісів,
    провайдерів та глобальні налаштування."""
    edit_index: int | None = None # Сховище для позиції елемента який редагується

    def __init__(self, app_config: AppConfig | None) -> None:
        self.tui_theme = app_config.theme if app_config else "bright"
        address_book_storage_provider = StorageProvider("contacts.json")
        self.address_book_manager = AddressBookService(address_book_storage_provider)
        notes_storage_provider = StorageProvider("notes.json")
        self.notes_manager = NotesService(notes_storage_provider)

    def get_stats(self) -> dict[str, int]:
        """Поточна кількість контактів та нотаток"""
        return {
            "contacts": len(self.address_book_manager.contacts),
            "notes": len(self.notes_manager.notes)
        }
