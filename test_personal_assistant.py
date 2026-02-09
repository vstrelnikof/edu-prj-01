"""
Тести для Персонального помічника (JSON версія)
"""
import unittest
import json
from datetime import datetime, timedelta
from pathlib import Path
from contacts import Name, Phone, Email, Birthday, Address, Record, AddressBook
from notes import Note, NoteBook
from command_parser import CommandParser


class TestFields(unittest.TestCase):
    """Тести для полів"""
    
    def test_name_creation(self):
        """Тест створення імені"""
        name = Name("Іван Петренко")
        self.assertEqual(str(name), "Іван Петренко")
    
    def test_empty_name(self):
        """Тест порожнього імені"""
        with self.assertRaises(ValueError):
            Name("   ")
    
    def test_valid_phone(self):
        """Тест валідного телефону"""
        phone = Phone("0991234567")
        self.assertEqual(phone.value, "0991234567")
    
    def test_invalid_phone(self):
        """Тест невалідного телефону"""
        with self.assertRaises(ValueError):
            Phone("099-123-45-67")
        
        with self.assertRaises(ValueError):
            Phone("123")
    
    def test_valid_email(self):
        """Тест валідного email"""
        email = Email("test@example.com")
        self.assertEqual(email.value, "test@example.com")
    
    def test_invalid_email(self):
        """Тест невалідного email"""
        with self.assertRaises(ValueError):
            Email("invalid.email")
        
        with self.assertRaises(ValueError):
            Email("test@")
    
    def test_valid_birthday(self):
        """Тест валідної дати народження"""
        birthday = Birthday("15.03.1990")
        self.assertEqual(birthday.value.year, 1990)
        self.assertEqual(birthday.value.month, 3)
        self.assertEqual(birthday.value.day, 15)
    
    def test_invalid_birthday(self):
        """Тест невалідної дати народження"""
        with self.assertRaises(ValueError):
            Birthday("32.13.2020")
        
        with self.assertRaises(ValueError):
            Birthday("15/03/1990")


class TestRecord(unittest.TestCase):
    """Тести для запису контакту"""
    
    def setUp(self):
        """Підготовка до тестів"""
        self.record = Record("Іван Петренко")
    
    def test_record_creation(self):
        """Тест створення запису"""
        self.assertEqual(self.record.name.value, "Іван Петренко")
        self.assertEqual(len(self.record.phones), 0)
    
    def test_add_phone(self):
        """Тест додавання телефону"""
        self.record.add_phone("0991234567")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "0991234567")
    
    def test_remove_phone(self):
        """Тест видалення телефону"""
        self.record.add_phone("0991234567")
        self.record.add_phone("0501234567")
        self.record.remove_phone("0991234567")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "0501234567")
    
    def test_edit_phone(self):
        """Тест редагування телефону"""
        self.record.add_phone("0991234567")
        self.record.edit_phone("0991234567", "0501234567")
        self.assertEqual(self.record.phones[0].value, "0501234567")
    
    def test_add_email(self):
        """Тест додавання email"""
        self.record.add_email("test@example.com")
        self.assertEqual(self.record.email.value, "test@example.com")
    
    def test_add_birthday(self):
        """Тест додавання дня народження"""
        self.record.add_birthday("15.03.1990")
        self.assertEqual(self.record.birthday.value.day, 15)
    
    def test_days_to_birthday(self):
        """Тест розрахунку днів до дня народження"""
        # Створюємо день народження через 10 днів
        future_date = datetime.now().date() + timedelta(days=10)
        birthday_str = future_date.strftime("%d.%m.") + str(1990)
        
        self.record.add_birthday(birthday_str)
        days = self.record.days_to_birthday()
        
        self.assertIsNotNone(days)
        self.assertGreaterEqual(days, 0)
    
    def test_to_dict(self):
        """Тест серіалізації в словник (для JSON)"""
        self.record.add_phone("0991234567")
        self.record.add_email("test@example.com")
        self.record.add_address("Київ")
        
        data = self.record.to_dict()
        
        self.assertEqual(data['name'], "Іван Петренко")
        self.assertEqual(len(data['phones']), 1)
        self.assertEqual(data['email'], "test@example.com")
        self.assertEqual(data['address'], "Київ")
    
    def test_from_dict(self):
        """Тест десеріалізації зі словника (з JSON)"""
        data = {
            'name': 'Іван Петренко',
            'phones': ['0991234567', '0501234567'],
            'email': 'test@example.com',
            'birthday': '15.03.1990',
            'address': 'Київ'
        }
        
        record = Record.from_dict(data)
        
        self.assertEqual(record.name.value, 'Іван Петренко')
        self.assertEqual(len(record.phones), 2)
        self.assertEqual(record.email.value, 'test@example.com')
        self.assertIsNotNone(record.birthday)
        self.assertEqual(record.address.value, 'Київ')


class TestAddressBook(unittest.TestCase):
    """Тести для адресної книги"""
    
    def setUp(self):
        """Підготовка до тестів"""
        self.book = AddressBook()
        # Використовуємо тестовий файл
        self.book.data_file = Path("test_contacts.json")
    
    def tearDown(self):
        """Очищення після тестів"""
        if self.book.data_file.exists():
            self.book.data_file.unlink()
    
    def test_add_record(self):
        """Тест додавання запису"""
        record = Record("Іван Петренко")
        self.book.add_record(record)
        self.assertIn("Іван Петренко", self.book.data)
    
    def test_find_record(self):
        """Тест пошуку запису"""
        record = Record("Іван Петренко")
        self.book.add_record(record)
        found = self.book.find("Іван Петренко")
        self.assertIsNotNone(found)
        self.assertEqual(found.name.value, "Іван Петренко")
    
    def test_delete_record(self):
        """Тест видалення запису"""
        record = Record("Іван Петренко")
        self.book.add_record(record)
        self.book.delete("Іван Петренко")
        self.assertNotIn("Іван Петренко", self.book.data)
    
    def test_search(self):
        """Тест пошуку"""
        record1 = Record("Іван Петренко")
        record1.add_phone("0991234567")
        
        record2 = Record("Марія Коваль")
        record2.add_email("maria@example.com")
        
        self.book.add_record(record1)
        self.book.add_record(record2)
        
        # Пошук за ім'ям
        results = self.book.search("Іван")
        self.assertEqual(len(results), 1)
        
        # Пошук за телефоном
        results = self.book.search("0991234567")
        self.assertEqual(len(results), 1)
        
        # Пошук за email
        results = self.book.search("maria")
        self.assertEqual(len(results), 1)
    
    def test_json_save_and_load(self):
        """Тест збереження та завантаження JSON"""
        record1 = Record("Іван Петренко")
        record1.add_phone("0991234567")
        record1.add_email("ivan@example.com")
        record1.add_address("Київ")
        
        record2 = Record("Марія Коваль")
        record2.add_phone("0501234567")
        
        self.book.add_record(record1)
        self.book.add_record(record2)
        self.book.save()
        
        # Перевіряємо що файл існує та є валідним JSON
        self.assertTrue(self.book.data_file.exists())
        
        with open(self.book.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 2)
        
        # Завантажуємо в нову книгу
        new_book = AddressBook()
        new_book.data_file = self.book.data_file
        new_book.load()
        
        self.assertEqual(len(new_book.data), 2)
        self.assertIn("Іван Петренко", new_book.data)
        self.assertIn("Марія Коваль", new_book.data)
        
        found = new_book.find("Іван Петренко")
        self.assertEqual(found.email.value, "ivan@example.com")
        self.assertEqual(len(found.phones), 1)


class TestNote(unittest.TestCase):
    """Тести для нотаток"""
    
    def test_note_creation(self):
        """Тест створення нотатки"""
        note = Note("Тестова нотатка", "Це тестовий текст")
        self.assertEqual(note.title, "Тестова нотатка")
        self.assertEqual(note.content, "Це тестовий текст")
        self.assertEqual(len(note.tags), 0)
    
    def test_add_tag(self):
        """Тест додавання тегу"""
        note = Note("Нотатка", "Текст")
        note.add_tag("важливо")
        self.assertIn("важливо", note.tags)
    
    def test_remove_tag(self):
        """Тест видалення тегу"""
        note = Note("Нотатка", "Текст")
        note.add_tag("важливо")
        note.remove_tag("важливо")
        self.assertNotIn("важливо", note.tags)
    
    def test_edit_note(self):
        """Тест редагування нотатки"""
        note = Note("Стара назва", "Старий текст")
        note.edit(title="Нова назва", content="Новий текст")
        self.assertEqual(note.title, "Нова назва")
        self.assertEqual(note.content, "Новий текст")
    
    def test_to_dict(self):
        """Тест серіалізації нотатки (для JSON)"""
        note = Note("Тест", "Текст")
        note.add_tag("робота")
        
        data = note.to_dict()
        
        self.assertEqual(data['title'], "Тест")
        self.assertEqual(data['content'], "Текст")
        self.assertIn('робота', data['tags'])
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_from_dict(self):
        """Тест десеріалізації нотатки (з JSON)"""
        data = {
            'title': 'Тест',
            'content': 'Текст',
            'tags': ['робота', 'важливо'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        note = Note.from_dict(data)
        
        self.assertEqual(note.title, 'Тест')
        self.assertEqual(len(note.tags), 2)


class TestNoteBook(unittest.TestCase):
    """Тести для блокноту"""
    
    def setUp(self):
        """Підготовка до тестів"""
        self.notebook = NoteBook()
        # Використовуємо тестовий файл
        self.notebook.data_file = Path("test_notes.json")
    
    def tearDown(self):
        """Очищення після тестів"""
        if self.notebook.data_file.exists():
            self.notebook.data_file.unlink()
    
    def test_add_note(self):
        """Тест додавання нотатки"""
        note = Note("Тест", "Текст")
        self.notebook.add_note(note)
        self.assertEqual(len(self.notebook.notes), 1)
    
    def test_delete_note(self):
        """Тест видалення нотатки"""
        note = Note("Тест", "Текст")
        self.notebook.add_note(note)
        result = self.notebook.delete_note(0)
        self.assertTrue(result)
        self.assertEqual(len(self.notebook.notes), 0)
    
    def test_search(self):
        """Тест пошуку"""
        note1 = Note("Python", "Мова програмування")
        note2 = Note("JavaScript", "Веб розробка")
        
        self.notebook.add_note(note1)
        self.notebook.add_note(note2)
        
        results = self.notebook.search("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1].title, "Python")
    
    def test_search_by_tag(self):
        """Тест пошуку за тегом"""
        note1 = Note("Нотатка 1", "Текст 1")
        note1.add_tag("робота")
        
        note2 = Note("Нотатка 2", "Текст 2")
        note2.add_tag("особисте")
        
        self.notebook.add_note(note1)
        self.notebook.add_note(note2)
        
        results = self.notebook.search_by_tag("робота")
        self.assertEqual(len(results), 1)
    
    def test_get_all_tags(self):
        """Тест отримання всіх тегів"""
        note1 = Note("Нотатка 1", "Текст 1")
        note1.add_tag("робота")
        note1.add_tag("проект")
        
        note2 = Note("Нотатка 2", "Текст 2")
        note2.add_tag("особисте")
        
        self.notebook.add_note(note1)
        self.notebook.add_note(note2)
        
        tags = self.notebook.get_all_tags()
        self.assertEqual(len(tags), 3)
        self.assertIn("робота", tags)
        self.assertIn("проект", tags)
        self.assertIn("особисте", tags)
    
    def test_json_save_and_load(self):
        """Тест збереження та завантаження JSON"""
        note1 = Note("Тест 1", "Текст 1")
        note1.add_tag("робота")
        note1.add_tag("проект")
        
        note2 = Note("Тест 2", "Текст 2")
        note2.add_tag("особисте")
        
        self.notebook.add_note(note1)
        self.notebook.add_note(note2)
        self.notebook.save()
        
        # Перевіряємо що файл існує та є валідним JSON
        self.assertTrue(self.notebook.data_file.exists())
        
        with open(self.notebook.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 2)
        
        # Завантажуємо в новий блокнот
        new_notebook = NoteBook()
        new_notebook.data_file = self.notebook.data_file
        new_notebook.load()
        
        self.assertEqual(len(new_notebook.notes), 2)
        self.assertEqual(new_notebook.notes[0].title, "Тест 1")
        self.assertIn("робота", new_notebook.notes[0].tags)
        self.assertIn("проект", new_notebook.notes[0].tags)


class TestCommandParser(unittest.TestCase):
    """Тести для парсера команд"""
    
    def test_exact_match(self):
        """Тест точного співпадіння"""
        command, confidence = CommandParser.find_command("додати контакт")
        self.assertEqual(command, "add-contact")
        self.assertEqual(confidence, 1.0)
    
    def test_fuzzy_match(self):
        """Тест нечіткого співпадіння"""
        command, confidence = CommandParser.find_command("додати контант")
        self.assertEqual(command, "add-contact")
        self.assertGreater(confidence, 0.6)
    
    def test_no_match(self):
        """Тест відсутності співпадіння"""
        command, confidence = CommandParser.find_command("абракадабра")
        self.assertIsNone(command)
    
    def test_suggest_command(self):
        """Тест підказки команди"""
        command, level, confidence = CommandParser.suggest_command("показати контакт")
        self.assertEqual(command, "show-contact")
        self.assertEqual(level, "висока")


if __name__ == "__main__":
    # Запуск тестів з verbose output
    unittest.main(verbosity=2)
