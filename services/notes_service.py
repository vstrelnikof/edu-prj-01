from decorators.log_decorator import log_action
from models.note import Note
from providers.storage_provider import StorageProvider
from services.base_service import BaseService

class NotesService(BaseService):
    notes: list[Note]

    def __init__(self) -> None:
        self._reload()
    
    def find_note_by_id(self, id: str) -> (Note | None):
        return next((note for note in self.notes if note.id == id), None)

    @log_action
    def add_note(self, data: dict) -> None:
        new_note: Note = self.__get_note_from_dict(data)
        if not new_note.is_valid():
            return
        self.notes.append(new_note)
        self.save()
    
    @log_action
    def edit_note(self, index: int, data: dict) -> None:
        updated_note: Note = self.__get_note_from_dict(data)
        if not updated_note.is_valid():
            return
        self.notes[index] = updated_note
        self.save()

    @log_action
    def delete_note(self, index: int) -> None:
        self.notes.pop(index)
        self.save()
    
    def get_notes_table_data(self, search_term: str) -> list:
        table_data: list = []
        for i, note in enumerate(self.notes):
            is_relevant: bool = any([tag for tag in note.tags if search_term in tag.lower()])
            if not is_relevant:
                continue
            note_text: str = note.text.replace('\n', ' ')
            table_data.append(([(note_text[:60] + '...')
                                if len(note_text) > 60 else note_text,
                                note.tags_string], i))
        return table_data

    @log_action
    def save(self) -> None:
        self.storage.save([n.__dict__ for n in self.notes])
    
    @log_action
    def _reload(self) -> None:
        self.storage = StorageProvider("notes.json")
        self.notes = [Note(**n) for n in self.storage.load()]
    
    def __get_note_from_dict(self, data: dict) -> Note:
        note = Note(data["text"])
        note.set_tags_from_string(data["tags"])
        return note