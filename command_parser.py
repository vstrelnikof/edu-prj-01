"""
Модуль для інтелектуального розпізнавання команд
"""
from difflib import get_close_matches


class CommandParser:
    """Клас для розпізнавання та підказки команд"""
    
    COMMANDS = {
        # Команди для контактів
        'add-contact': ['додати контакт', 'новий контакт', 'add contact', 'create contact'],
        'edit-contact': ['редагувати контакт', 'змінити контакт', 'edit contact', 'update contact'],
        'delete-contact': ['видалити контакт', 'delete contact', 'remove contact'],
        'show-contact': ['показати контакт', 'знайти контакт', 'show contact', 'find contact'],
        'all-contacts': ['всі контакти', 'список контактів', 'all contacts', 'list contacts'],
        'search-contacts': ['пошук контактів', 'шукати контакт', 'search contacts'],
        'birthdays': ['дні народження', 'birthdays', 'upcoming birthdays'],
        
        # Команди для нотаток
        'add-note': ['додати нотатку', 'нова нотатка', 'add note', 'create note'],
        'edit-note': ['редагувати нотатку', 'змінити нотатку', 'edit note', 'update note'],
        'delete-note': ['видалити нотатку', 'delete note', 'remove note'],
        'show-notes': ['показати нотатки', 'всі нотатки', 'show notes', 'list notes'],
        'search-notes': ['пошук нотаток', 'шукати нотатку', 'search notes', 'find notes'],
        'add-tag': ['додати тег', 'add tag'],
        'search-by-tag': ['пошук за тегом', 'search by tag', 'find by tag'],
        'show-tags': ['показати теги', 'всі теги', 'show tags', 'list tags'],
        
        # Загальні команди
        'help': ['допомога', 'help', 'commands', 'команди'],
        'exit': ['вийти', 'exit', 'quit', 'bye', 'close'],
    }

    @classmethod
    def get_all_command_variants(cls):
        """Отримання всіх варіантів команд"""
        all_variants = []
        for variants in cls.COMMANDS.values():
            all_variants.extend(variants)
        return all_variants

    @classmethod
    def find_command(cls, user_input):
        """Знаходження найближчої команди до введеного тексту"""
        user_input_lower = user_input.lower().strip()
        
        # Точний збіг
        for command, variants in cls.COMMANDS.items():
            if user_input_lower in variants:
                return command, 1.0  # 100% впевненість
        
        # Нечітке співставлення
        all_variants = cls.get_all_command_variants()
        matches = get_close_matches(user_input_lower, all_variants, n=1, cutoff=0.6)
        
        if matches:
            matched_variant = matches[0]
            for command, variants in cls.COMMANDS.items():
                if matched_variant in variants:
                    # Розрахунок впевненості
                    confidence = cls._calculate_confidence(user_input_lower, matched_variant)
                    return command, confidence
        
        return None, 0.0

    @staticmethod
    def _calculate_confidence(input_str, matched_str):
        """Розрахунок впевненості співставлення"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, input_str, matched_str).ratio()

    @classmethod
    def suggest_command(cls, user_input):
        """Підказка команди на основі введеного тексту"""
        command, confidence = cls.find_command(user_input)
        
        if command and confidence >= 0.8:
            return command, "висока", confidence
        elif command and confidence >= 0.6:
            return command, "середня", confidence
        else:
            # Пошук схожих команд
            all_variants = cls.get_all_command_variants()
            suggestions = get_close_matches(user_input.lower(), all_variants, n=3, cutoff=0.4)
            return None, "низька", suggestions

    @classmethod
    def get_command_help(cls, command=None):
        """Отримання довідки по команді"""
        help_text = {
            'add-contact': "Додати новий контакт з ім'ям, телефоном, email, адресою та днем народження",
            'edit-contact': "Редагувати існуючий контакт",
            'delete-contact': "Видалити контакт",
            'show-contact': "Показати інформацію про контакт",
            'all-contacts': "Показати всі контакти",
            'search-contacts': "Пошук контактів за різними критеріями",
            'birthdays': "Показати контакти з днями народження найближчим часом",
            
            'add-note': "Додати нову нотатку",
            'edit-note': "Редагувати нотатку",
            'delete-note': "Видалити нотатку",
            'show-notes': "Показати всі нотатки",
            'search-notes': "Пошук нотаток за текстом",
            'add-tag': "Додати тег до нотатки",
            'search-by-tag': "Пошук нотаток за тегом",
            'show-tags': "Показати всі теги",
            
            'help': "Показати довідку",
            'exit': "Вийти з програми",
        }
        
        if command:
            return help_text.get(command, "Команда не знайдена")
        else:
            return help_text
