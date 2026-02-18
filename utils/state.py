from datetime import datetime, timedelta
from managers.address_book_manager import AddressBookManager
from managers.notes_manager import NotesManager

class AppState:
    """Об'єкт стану, що зберігає всі менеджери та глобальні налаштування."""
    def __init__(self):
        self.tui_theme = "bright"
        self.address_book_manager = AddressBookManager()
        self.notes_manager = NotesManager()

    def get_stats(self):
        return {
            "contacts": len(self.address_book_manager.contacts),
            "notes": len(self.notes_manager.notes)
        }

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today()
        upcoming = []
        for c in self.address_book_manager.contacts:
            try:
                bday = datetime.strptime(c.birthday, "%Y-%m-%d")
                bday_this_year = bday.replace(year=today.year)
                if today <= bday_this_year <= today + timedelta(days=days):
                    upcoming.append(f"{c.name} ({bday_this_year.strftime('%d.%m')})")
            except (ValueError, TypeError):
                continue
        return upcoming if upcoming else ["На найближчий тиждень іменинників немає"]