#!/usr/bin/env python3
"""
Добавление колонок для ответственных органов в таблицу district_mappings
"""
import sqlite3

DB_PATH = 'land_records.db'

def add_columns():
    print("=" * 80)
    print("ДОБАВЛЕНИЕ КОЛОНОК В ТАБЛИЦУ district_mappings")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем текущую структуру таблицы
    print("\n1. Проверяю текущую структуру таблицы...")
    cursor.execute("PRAGMA table_info(district_mappings)")
    columns = cursor.fetchall()
    existing_columns = [col[1] for col in columns]
    print(f"   Существующие колонки: {existing_columns}")
    
    # Добавляем колонку responsible_org если её нет
    if 'responsible_org' not in existing_columns:
        print("\n2. Добавляю колонку 'responsible_org'...")
        cursor.execute("ALTER TABLE district_mappings ADD COLUMN responsible_org TEXT")
        print("   ✅ Колонка 'responsible_org' добавлена")
    else:
        print("\n2. ✅ Колонка 'responsible_org' уже существует")
    
    # Добавляем колонку org_address если её нет
    if 'org_address' not in existing_columns:
        print("\n3. Добавляю колонку 'org_address'...")
        cursor.execute("ALTER TABLE district_mappings ADD COLUMN org_address TEXT")
        print("   ✅ Колонка 'org_address' добавлена")
    else:
        print("\n3. ✅ Колонка 'org_address' уже существует")
    
    conn.commit()
    
    # Проверяем результат
    print("\n4. Проверяю финальную структуру...")
    cursor.execute("PRAGMA table_info(district_mappings)")
    columns = cursor.fetchall()
    print("   Колонки в таблице:")
    for col in columns:
        print(f"      - {col[1]} ({col[2]})")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ ГОТОВО! Колонки добавлены")
    print("=" * 80)

if __name__ == '__main__':
    add_columns()

