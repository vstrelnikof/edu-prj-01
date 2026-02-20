from enum import StrEnum
from typing import final

@final
class SceneType(StrEnum):
    """Типи сцен. Використовуються як унікальне ім'я для сцени."""
    MAIN = "Main"
    CONTACT_FORM = "ContactForm"
    CONTACTS_LIST = "ContactsList"
    NOTE_FORM = "NoteForm"
    NOTES_LIST = "NotesList"
    BIRTHDAYS_LIST  = "BirthDaysList"