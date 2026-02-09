"""
Персональний помічник - головний файл програми
"""
from contacts import AddressBook, Record
from notes import NoteBook, Note
from command_parser import CommandParser


class PersonalAssistant:
    """Головний клас персонального помічнпоика"""
    
    def __init__(self):
        self.address_book = AddressBook()
        self.notebook = NoteBook()
        self.parser = CommandParser()
        
        # Завантаження даних
        self.load_data()
    
    def load_data(self):
        """Завантаження всіх даних"""
        try:
            self.address_book.load()
            self.notebook.load()
            print("✓ Дані успішно завантажено")
        except Exception as e:
            print(f"⚠ Помилка завантаження даних: {e}")
    
    def save_data(self):
        """Збереження всіх даних"""
        try:
            self.address_book.save()
            self.notebook.save()
            print("✓ Дані успішно збережено")
        except Exception as e:
            print(f"⚠ Помилка збереження даних: {e}")
    
    # ==================== РОБОТА З КОНТАКТАМИ ====================
    
    def add_contact(self):
        """Додавання нового контакту"""
        print("\n=== Додавання нового контакту ===")
        
        name = input("Введіть ім'я: ").strip()
        if not name:
            print("❌ Ім'я не може бути порожнім")
            return
        
        if self.address_book.find(name):
            print(f"❌ Контакт з ім'ям '{name}' вже існує")
            return
        
        try:
            record = Record(name)
            
            # Телефон
            phone = input("Введіть телефон (10 цифр) або Enter для пропуску: ").strip()
            if phone:
                record.add_phone(phone)
            
            # Email
            email = input("Введіть email або Enter для пропуску: ").strip()
            if email:
                record.add_email(email)
            
            # Адреса
            address = input("Введіть адресу або Enter для пропуску: ").strip()
            if address:
                record.add_address(address)
            
            # День народження
            birthday = input("Введіть день народження (ДД.ММ.РРРР) або Enter для пропуску: ").strip()
            if birthday:
                record.add_birthday(birthday)
            
            self.address_book.add_record(record)
            print(f"✓ Контакт '{name}' успішно додано")
            self.save_data()
            
        except ValueError as e:
            print(f"❌ Помилка: {e}")
    
    def edit_contact(self):
        """Редагування контакту"""
        print("\n=== Редагування контакту ===")
        
        name = input("Введіть ім'я контакту: ").strip()
        record = self.address_book.find(name)
        
        if not record:
            print(f"❌ Контакт '{name}' не знайдено")
            return
        
        print(f"\nПоточні дані:\n{record}\n")
        
        while True:
            print("\nЩо ви хочете змінити?")
            print("1. Додати телефон")
            print("2. Видалити телефон")
            print("3. Змінити email")
            print("4. Змінити адресу")
            print("5. Змінити день народження")
            print("0. Завершити редагування")
            
            choice = input("\nВиберіть опцію: ").strip()
            
            try:
                if choice == "1":
                    phone = input("Введіть новий телефон: ").strip()
                    record.add_phone(phone)
                    print("✓ Телефон додано")
                
                elif choice == "2":
                    phone = input("Введіть телефон для видалення: ").strip()
                    record.remove_phone(phone)
                    print("✓ Телефон видалено")
                
                elif choice == "3":
                    email = input("Введіть новий email: ").strip()
                    record.add_email(email)
                    print("✓ Email оновлено")
                
                elif choice == "4":
                    address = input("Введіть нову адресу: ").strip()
                    record.add_address(address)
                    print("✓ Адресу оновлено")
                
                elif choice == "5":
                    birthday = input("Введіть новий день народження (ДД.ММ.РРРР): ").strip()
                    record.add_birthday(birthday)
                    print("✓ День народження оновлено")
                
                elif choice == "0":
                    break
                
                else:
                    print("❌ Невірний вибір")
                    
            except ValueError as e:
                print(f"❌ Помилка: {e}")
        
        self.save_data()
        print(f"\n✓ Контакт оновлено:\n{record}")
    
    def delete_contact(self):
        """Видалення контакту"""
        print("\n=== Видалення контакту ===")
        
        name = input("Введіть ім'я контакту для видалення: ").strip()
        record = self.address_book.find(name)
        
        if not record:
            print(f"❌ Контакт '{name}' не знайдено")
            return
        
        confirm = input(f"Ви впевнені, що хочете видалити '{name}'? (так/ні): ").strip().lower()
        
        if confirm == "так":
            self.address_book.delete(name)
            self.save_data()
            print(f"✓ Контакт '{name}' видалено")
        else:
            print("Видалення скасовано")
    
    def show_contact(self):
        """Показати контакт"""
        print("\n=== Показати контакт ===")
        
        name = input("Введіть ім'я контакту: ").strip()
        record = self.address_book.find(name)
        
        if record:
            print(f"\n{record}")
        else:
            print(f"❌ Контакт '{name}' не знайдено")
    
    def show_all_contacts(self):
        """Показати всі контакти"""
        print("\n=== Всі контакти ===")
        
        if not self.address_book.data:
            print("📭 Книга контактів порожня")
            return
        
        for i, record in enumerate(self.address_book.data.values(), 1):
            print(f"\n{i}. {record}")
    
    def search_contacts(self):
        """Пошук контактів"""
        print("\n=== Пошук контактів ===")
        
        query = input("Введіть пошуковий запит: ").strip()
        
        if not query:
            print("❌ Запит не може бути порожнім")
            return
        
        results = self.address_book.search(query)
        
        if results:
            print(f"\n✓ Знайдено {len(results)} контакт(ів):\n")
            for i, record in enumerate(results, 1):
                print(f"{i}. {record}")
        else:
            print("❌ Нічого не знайдено")
    
    def show_birthdays(self):
        """Показати контакти з днями народження"""
        print("\n=== Дні народження ===")
        
        try:
            days = int(input("Введіть кількість днів (наприклад, 7 для тижня): ").strip())
            
            if days < 0:
                print("❌ Кількість днів не може бути від'ємною")
                return
            
            results = self.address_book.get_birthdays_in_days(days)
            
            if results:
                print(f"\n✓ Контакти з днями народження в найближчі {days} днів:\n")
                for record, days_left in results:
                    if days_left == 0:
                        print(f"🎉 СЬОГОДНІ: {record.name.value}")
                    elif days_left == 1:
                        print(f"🎂 Завтра: {record.name.value}")
                    else:
                        print(f"📅 Через {days_left} днів: {record.name.value}")
                    if record.birthday:
                        print(f"   Дата: {record.birthday.value.strftime('%d.%m.%Y')}")
            else:
                print(f"❌ Немає днів народження в найближчі {days} днів")
                
        except ValueError:
            print("❌ Будь ласка, введіть коректне число")
    
    # ==================== РОБОТА З НОТАТКАМИ ====================
    
    def add_note(self):
        """Додавання нотатки"""
        print("\n=== Додавання нотатки ===")
        
        title = input("Введіть назву нотатки: ").strip()
        if not title:
            print("❌ Назва не може бути порожньою")
            return
        
        content = input("Введіть текст нотатки: ").strip()
        if not content:
            print("❌ Текст не може бути порожнім")
            return
        
        note = Note(title, content)
        
        # Додавання тегів
        tags_input = input("Введіть теги через кому (або Enter для пропуску): ").strip()
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            for tag in tags:
                note.add_tag(tag)
        
        self.notebook.add_note(note)
        self.save_data()
        print("✓ Нотатку додано")
    
    def edit_note(self):
        """Редагування нотатки"""
        print("\n=== Редагування нотатки ===")
        
        self.show_notes()
        
        try:
            index = int(input("\nВведіть номер нотатки для редагування: ").strip()) - 1
            note = self.notebook.find_note(index)
            
            if not note:
                print("❌ Нотатку не знайдено")
                return
            
            print(f"\nПоточна нотатка:\n{note}\n")
            
            title = input("Нова назва (Enter для збереження поточної): ").strip()
            content = input("Новий текст (Enter для збереження поточного): ").strip()
            
            note.edit(title if title else None, content if content else None)
            self.save_data()
            print("✓ Нотатку оновлено")
            
        except (ValueError, IndexError):
            print("❌ Невірний номер нотатки")
    
    def delete_note(self):
        """Видалення нотатки"""
        print("\n=== Видалення нотатки ===")
        
        self.show_notes()
        
        try:
            index = int(input("\nВведіть номер нотатки для видалення: ").strip()) - 1
            
            if self.notebook.delete_note(index):
                self.save_data()
                print("✓ Нотатку видалено")
            else:
                print("❌ Нотатку не знайдено")
                
        except (ValueError, IndexError):
            print("❌ Невірний номер нотатки")
    
    def show_notes(self):
        """Показати всі нотатки"""
        if not self.notebook.notes:
            print("📭 Нотаток немає")
            return
        
        print("\n=== Всі нотатки ===")
        for i, note in enumerate(self.notebook.notes, 1):
            print(f"\n{i}. {note}")
    
    def search_notes(self):
        """Пошук нотаток"""
        print("\n=== Пошук нотаток ===")
        
        query = input("Введіть пошуковий запит: ").strip()
        
        if not query:
            print("❌ Запит не може бути порожнім")
            return
        
        results = self.notebook.search(query)
        
        if results:
            print(f"\n✓ Знайдено {len(results)} нотаток:\n")
            for index, note in results:
                print(f"{index + 1}. {note}")
        else:
            print("❌ Нічого не знайдено")
    
    def add_tag_to_note(self):
        """Додавання тегу до нотатки"""
        print("\n=== Додавання тегу ===")
        
        self.show_notes()
        
        try:
            index = int(input("\nВведіть номер нотатки: ").strip()) - 1
            note = self.notebook.find_note(index)
            
            if not note:
                print("❌ Нотатку не знайдено")
                return
            
            tag = input("Введіть тег: ").strip()
            if tag:
                note.add_tag(tag)
                self.save_data()
                print("✓ Тег додано")
            else:
                print("❌ Тег не може бути порожнім")
                
        except (ValueError, IndexError):
            print("❌ Невірний номер нотатки")
    
    def search_by_tag(self):
        """Пошук нотаток за тегом"""
        print("\n=== Пошук за тегом ===")
        
        # Показати доступні теги
        tags = self.notebook.get_all_tags()
        if tags:
            print(f"Доступні теги: {', '.join(tags)}")
        
        tag = input("\nВведіть тег для пошуку: ").strip()
        
        if not tag:
            print("❌ Тег не може бути порожнім")
            return
        
        results = self.notebook.search_by_tag(tag)
        
        if results:
            print(f"\n✓ Знайдено {len(results)} нотаток з тегом '{tag}':\n")
            for index, note in results:
                print(f"{index + 1}. {note}")
        else:
            print(f"❌ Нотаток з тегом '{tag}' не знайдено")
    
    def show_all_tags(self):
        """Показати всі теги"""
        print("\n=== Всі теги ===")
        
        tags = self.notebook.get_all_tags()
        
        if tags:
            print(f"\n✓ Всього тегів: {len(tags)}")
            for tag in tags:
                count = sum(1 for note in self.notebook.notes if tag in note.tags)
                print(f"  • {tag} ({count} нотаток)")
        else:
            print("📭 Тегів немає")
    
    # ==================== ГОЛОВНЕ МЕНЮ ====================
    
    def show_menu(self):
        """Показати головне меню"""
        print("\n" + "="*50)
        print("📚 ПЕРСОНАЛЬНИЙ ПОМІЧНИК")
        print("="*50)
        print("\n🔹 КОНТАКТИ:")
        print("  1.  Додати контакт")
        print("  2.  Редагувати контакт")
        print("  3.  Видалити контакт")
        print("  4.  Показати контакт")
        print("  5.  Всі контакти")
        print("  6.  Пошук контактів")
        print("  7.  Дні народження")
        
        print("\n🔹 НОТАТКИ:")
        print("  8.  Додати нотатку")
        print("  9.  Редагувати нотатку")
        print("  10. Видалити нотатку")
        print("  11. Показати нотатки")
        print("  12. Пошук нотаток")
        print("  13. Додати тег до нотатки")
        print("  14. Пошук за тегом")
        print("  15. Показати всі теги")
        
        print("\n🔹 ІНШЕ:")
        print("  0.  Вийти")
        print("="*50)
    
    def run(self):
        """Запуск помічника"""
        print("\n🎉 Вітаємо у Персональному помічнику! 🎉\n")
        
        while True:
            self.show_menu()
            
            choice = input("\n💬 Введіть номер команди або опишіть що ви хочете зробити: ").strip()
            
            # Спроба розпізнати текстову команду
            if not choice.isdigit():
                command, confidence_level, confidence = self.parser.suggest_command(choice)
                
                if command and confidence >= 0.6:
                    print(f"\n💡 Схоже ви хочете: {self.parser.get_command_help(command)}")
                    confirm = input("Виконати цю команду? (так/ні): ").strip().lower()
                    
                    if confirm != "так":
                        continue
                    
                    # Мапінг команд на методи
                    command_map = {
                        'add-contact': '1',
                        'edit-contact': '2',
                        'delete-contact': '3',
                        'show-contact': '4',
                        'all-contacts': '5',
                        'search-contacts': '6',
                        'birthdays': '7',
                        'add-note': '8',
                        'edit-note': '9',
                        'delete-note': '10',
                        'show-notes': '11',
                        'search-notes': '12',
                        'add-tag': '13',
                        'search-by-tag': '14',
                        'show-tags': '15',
                        'exit': '0',
                    }
                    
                    choice = command_map.get(command, '')
                else:
                    print("❌ Команду не розпізнано. Спробуйте ввести номер з меню.")
                    continue
            
            # Виконання команди
            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.edit_contact()
            elif choice == "3":
                self.delete_contact()
            elif choice == "4":
                self.show_contact()
            elif choice == "5":
                self.show_all_contacts()
            elif choice == "6":
                self.search_contacts()
            elif choice == "7":
                self.show_birthdays()
            elif choice == "8":
                self.add_note()
            elif choice == "9":
                self.edit_note()
            elif choice == "10":
                self.delete_note()
            elif choice == "11":
                self.show_notes()
            elif choice == "12":
                self.search_notes()
            elif choice == "13":
                self.add_tag_to_note()
            elif choice == "14":
                self.search_by_tag()
            elif choice == "15":
                self.show_all_tags()
            elif choice == "0":
                print("\n👋 До побачення!")
                self.save_data()
                break
            else:
                print("❌ Невірний вибір. Спробуйте ще раз.")


def main():
    """Головна функція"""
    assistant = PersonalAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
