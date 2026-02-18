from decorators.log_decorator import log_action
from models.note import Note
from managers.storage_manager import StorageManager

class NotesManager:
    def __init__(self):
        self.storage = StorageManager("notes.json")
        self.notes = [Note(**n) for n in self.storage.load()]

    @log_action
    def add_note(self):
        text = input("Текст нотатки: ")
        tags = input("Теги (через кому): ").split(",")
        note = Note(text, [t.strip() for t in tags if t.strip()])
        self.notes.append(note)
        self.save()
        print("✅ Нотатка додана!")
    
    def add_note_from_dict(self, data: dict):
        new_note = Note(text=data["text"], tags=data["tags"])
        self.notes.append(new_note)
        self.save()

    @log_action
    def list_notes(self):
        for n in self.notes:
            print(n)

    @log_action
    def search_note(self):
        query = input("Введіть ключове слово або тег: ").lower()
        results = [n for n in self.notes if query in n.text.lower() or query in [t.lower() for t in n.tags]]
        print("\n".join(map(str, results)) if results else "❌ Нотатка не знайдена")

    @log_action
    def edit_note(self):
        text = input("Введіть текст нотатки для редагування: ")
        for n in self.notes:
            if n.text.lower() == text.lower():
                n.text = input(f"Новий текст ({n.text}): ") or n.text
                tags = input(f"Нові теги ({', '.join(n.tags)}): ")
                if tags:
                    n.tags = [t.strip() for t in tags.split(",")]
                self.save()
                print("✅ Нотатка оновлена!")
                return
        print("❌ Нотатка не знайдена")

    @log_action
    def delete_note(self):
        text = input("Введіть текст нотатки для видалення: ")
        self.notes = [n for n in self.notes if n.text.lower() != text.lower()]
        self.save()
        print("✅ Нотатка видалена!")

    @log_action
    def save(self):
        self.storage.save([n.__dict__ for n in self.notes])