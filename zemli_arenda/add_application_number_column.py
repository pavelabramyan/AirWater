#!/usr/bin/env python3
"""
Скрипт для добавления колонки 'application_number' в таблицу land_records
"""

import sqlite3
import os

DB_PATH = 'land_records.db'

def add_application_number_column():
    """Добавить колонку для хранения номера заявления"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ База данных {DB_PATH} не найдена!")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Проверяем, существует ли уже колонка
        cursor.execute("PRAGMA table_info(land_records)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'application_number' in columns:
            print("ℹ️  Колонка 'application_number' уже существует")
            return True
        
        # Добавляем колонку
        print("📝 Добавляю колонку 'application_number'...")
        cursor.execute("""
            ALTER TABLE land_records 
            ADD COLUMN application_number TEXT DEFAULT NULL
        """)
        
        conn.commit()
        print("✅ Колонка 'application_number' успешно добавлена!")
        
        # Проверяем результат
        cursor.execute("PRAGMA table_info(land_records)")
        columns = cursor.fetchall()
        print(f"\n📊 Всего колонок в таблице: {len(columns)}")
        
        # Показываем последние колонки
        print("\n📋 Последние колонки:")
        for col in columns[-5:]:
            col_id, name, col_type, not_null, default, pk = col
            print(f"   {name} ({col_type})")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка при добавлении колонки: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == '__main__':
    print("="*80)
    print("🔧 ДОБАВЛЕНИЕ КОЛОНКИ 'application_number'")
    print("="*80)
    
    success = add_application_number_column()
    
    if success:
        print("\n✅ Готово! Теперь можно запускать скрипт отправки заявлений.")
    else:
        print("\n❌ Не удалось добавить колонку. Проверьте ошибки выше.")

