"""
Модуль для роботи з нотатками
"""
from datetime import datetime
import json
from pathlib import Path


class Note:
    """Клас для зберігання нотатки"""
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_tag(self, tag):
        """Додавання тегу"""
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.now()

    def remove_tag(self, tag):
        """Видалення тегу"""
        if tag.lower() in self.tags:
            self.tags.remove(tag.lower())
            self.updated_at = datetime.now()

    def edit(self, title=None, content=None):
        """Редагування нотатки"""
        if title:
            self.title = title
        if content:
            self.content = content
        self.updated_at = datetime.now()

    def to_dict(self):
        """Серіалізація нотатки в словник для JSON"""
        return {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """Десеріалізація нотатки зі словника JSON"""
        note = Note(data['title'], data['content'])
        note.tags = data.get('tags', [])
        note.created_at = datetime.fromisoformat(data['created_at'])
        note.updated_at = datetime.fromisoformat(data['updated_at'])
        return note

    def __str__(self):
        tags_str = f", теги: [{', '.join(self.tags)}]" if self.tags else ""
        return (f"📝 {self.title}\n"
                f"   {self.content}\n"
                f"   Створено: {self.created_at.strftime('%d.%m.%Y %H:%M')}"
                f"{tags_str}")


class NoteBook:
    """Клас для зберігання та управління нотатками"""
    def __init__(self):
        self.notes = []
        self.data_file = Path.home() / "personal_assistant_data" / "notes.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

    def add_note(self, note):
        """Додавання нотатки"""
        self.notes.append(note)

    def delete_note(self, index):
        """Видалення нотатки за індексом"""
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return True
        return False

    def find_note(self, index):
        """Пошук нотатки за індексом"""
        if 0 <= index < len(self.notes):
            return self.notes[index]
        return None

    def search(self, query):
        """Пошук нотаток за текстом"""
        results = []
        query_lower = query.lower()
        
        for i, note in enumerate(self.notes):
            if (query_lower in note.title.lower() or 
                query_lower in note.content.lower()):
                results.append((i, note))
        
        return results

    def search_by_tag(self, tag):
        """Пошук нотаток за тегом"""
        results = []
        tag_lower = tag.lower()
        
        for i, note in enumerate(self.notes):
            if tag_lower in note.tags:
                results.append((i, note))
        
        return results

    def get_all_tags(self):
        """Отримання всіх унікальних тегів"""
        tags = set()
        for note in self.notes:
            tags.update(note.tags)
        return sorted(tags)

    def sort_by_tags(self, tag=None):
        """Сортування нотаток за тегами"""
        if tag:
            # Сортування: спочатку нотатки з вказаним тегом
            tag_lower = tag.lower()
            return sorted(
                enumerate(self.notes),
                key=lambda x: (tag_lower not in x[1].tags, x[1].updated_at),
                reverse=True
            )
        else:
            # Сортування за кількістю тегів
            return sorted(
                enumerate(self.notes),
                key=lambda x: len(x[1].tags),
                reverse=True
            )

    def save(self):
        """Збереження нотаток на диск у JSON форматі"""
        notes_list = [note.to_dict() for note in self.notes]
        
        # Атомарне збереження через тимчасовий файл
        temp_file = self.data_file.with_suffix('.tmp')
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(notes_list, f, ensure_ascii=False, indent=2)
            
            # Атомарна заміна
            temp_file.replace(self.data_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise e

    def load(self):
        """Завантаження нотаток з диска"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    notes_list = json.load(f)
                
                self.notes.clear()
                for note_data in notes_list:
                    note = Note.from_dict(note_data)
                    self.notes.append(note)
            except json.JSONDecodeError as e:
                print(f"⚠️  Помилка читання файлу даних: {e}")
                print("Створюється новий блокнот")
                self.notes.clear()
