#!/usr/bin/env python3
"""
Скрипт міграції даних з pickle в JSON формат
Використовується для конвертації старих даних у новий формат
"""

import pickle
import json
from pathlib import Path
from datetime import datetime


def migrate_contacts():
    """Міграція контактів з pickle в JSON"""
    old_file = Path.home() / "personal_assistant_data" / "contacts.pkl"
    new_file = Path.home() / "personal_assistant_data" / "contacts.json"
    
    if not old_file.exists():
        print(f"⚠️  Файл {old_file} не знайдено. Пропускаємо міграцію контактів.")
        return False
    
    if new_file.exists():
        response = input(f"❓ Файл {new_file} вже існує. Перезаписати? (так/ні): ")
        if response.lower() not in ['так', 'yes', 'y', 'т']:
            print("❌ Міграція контактів скасована.")
            return False
    
    try:
        # Читаємо pickle
        print(f"📖 Читаємо {old_file}...")
        with open(old_file, 'rb') as f:
            old_data = pickle.load(f)
        
        # Конвертуємо
        contacts_list = []
        for name, record in old_data.items():
            contact_dict = {
                'name': record.name.value,
                'phones': [phone.value for phone in record.phones],
                'email': record.email.value if record.email else None,
                'birthday': record.birthday.value.strftime('%d.%m.%Y') if record.birthday else None,
                'address': record.address.value if record.address else None
            }
            contacts_list.append(contact_dict)
        
        # Зберігаємо JSON
        print(f"💾 Зберігаємо у JSON формат...")
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(contacts_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Контакти успішно мігровано: {len(contacts_list)} записів")
        
        # Створюємо backup
        backup_file = old_file.with_suffix('.pkl.backup')
        old_file.rename(backup_file)
        print(f"💾 Створено backup: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка міграції контактів: {e}")
        return False


def migrate_notes():
    """Міграція нотаток з pickle в JSON"""
    old_file = Path.home() / "personal_assistant_data" / "notes.pkl"
    new_file = Path.home() / "personal_assistant_data" / "notes.json"
    
    if not old_file.exists():
        print(f"⚠️  Файл {old_file} не знайдено. Пропускаємо міграцію нотаток.")
        return False
    
    if new_file.exists():
        response = input(f"❓ Файл {new_file} вже існує. Перезаписати? (так/ні): ")
        if response.lower() not in ['так', 'yes', 'y', 'т']:
            print("❌ Міграція нотаток скасована.")
            return False
    
    try:
        # Читаємо pickle
        print(f"📖 Читаємо {old_file}...")
        with open(old_file, 'rb') as f:
            old_notes = pickle.load(f)
        
        # Конвертуємо
        notes_list = []
        for note in old_notes:
            note_dict = {
                'title': note.title,
                'content': note.content,
                'tags': note.tags,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            }
            notes_list.append(note_dict)
        
        # Зберігаємо JSON
        print(f"💾 Зберігаємо у JSON формат...")
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(notes_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Нотатки успішно мігровано: {len(notes_list)} записів")
        
        # Створюємо backup
        backup_file = old_file.with_suffix('.pkl.backup')
        old_file.rename(backup_file)
        print(f"💾 Створено backup: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка міграції нотаток: {e}")
        return False


def main():
    """Головна функція міграції"""
    print("=" * 60)
    print("🔄 МІГРАЦІЯ ДАНИХ: pickle → JSON")
    print("=" * 60)
    print()
    print("Цей скрипт конвертує ваші дані зі старого формату (pickle)")
    print("у новий формат (JSON).")
    print()
    print("Переваги JSON:")
    print("  ✅ Читабельність - можна відкрити у текстовому редакторі")
    print("  ✅ Безпека - не може виконувати код")
    print("  ✅ Сумісність - працює на всіх платформах")
    print()
    
    data_dir = Path.home() / "personal_assistant_data"
    if not data_dir.exists():
        print(f"⚠️  Директорія {data_dir} не знайдена.")
        print("Можливо, ви ще не користувалися програмою.")
        return
    
    print(f"📂 Директорія даних: {data_dir}")
    print()
    
    # Перевіряємо які файли існують
    pkl_files = list(data_dir.glob("*.pkl"))
    if not pkl_files:
        print("⚠️  Не знайдено жодного .pkl файлу для міграції.")
        print("Можливо, дані вже мігровано.")
        return
    
    print(f"Знайдено {len(pkl_files)} файл(ів) для міграції:")
    for f in pkl_files:
        print(f"  • {f.name}")
    print()
    
    response = input("❓ Почати міграцію? (так/ні): ")
    if response.lower() not in ['так', 'yes', 'y', 'т']:
        print("❌ Міграцію скасовано.")
        return
    
    print()
    print("-" * 60)
    
    # Міграція
    contacts_ok = migrate_contacts()
    print()
    notes_ok = migrate_notes()
    
    # Підсумок
    print()
    print("=" * 60)
    print("📊 ПІДСУМОК МІГРАЦІЇ")
    print("=" * 60)
    
    if contacts_ok:
        print("✅ Контакти: успішно мігровано")
    else:
        print("❌ Контакти: міграція не виконана")
    
    if notes_ok:
        print("✅ Нотатки: успішно мігровано")
    else:
        print("❌ Нотатки: міграція не виконана")
    
    if contacts_ok or notes_ok:
        print()
        print("💡 Старі .pkl файли перейменовано в .pkl.backup")
        print("   Ви можете видалити їх після перевірки нових даних.")
        print()
        print("✅ Міграція завершена!")
        print("   Тепер запустіть main.py для роботи з оновленою програмою.")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Міграцію перервано користувачем")
    except Exception as e:
        print(f"\n❌ Несподівана помилка: {e}")
