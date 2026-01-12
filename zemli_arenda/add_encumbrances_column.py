#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления колонки 'encumbrances' (обременения) в БД
"""

import sqlite3

DB_PATH = "land_records.db"

def add_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Добавляем колонку для хранения обременений
        cursor.execute("ALTER TABLE land_records ADD COLUMN encumbrances TEXT")
        conn.commit()
        print("✅ Колонка 'encumbrances' успешно добавлена!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️  Колонка 'encumbrances' уже существует.")
        else:
            print(f"❌ Ошибка при добавлении колонки: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*80)
    print("🔧 ДОБАВЛЕНИЕ КОЛОНКИ 'encumbrances'")
    print("="*80)
    add_column()
    print("\n✅ Готово!")
    print("="*80)
    print("\n📋 Доступные статусы:")
    print("  - Не отправлена")
    print("  - Отправлено")
    print("  - Ошибка")
    print("  - Район не определен")
    print("  - Прервано")
    print("  - Занят (новый)")
    print("  - Не найден на Росреестре (новый)")
    print("="*80)



