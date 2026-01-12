#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки уникальности записей в БД НСПД
Помогает обнаружить дубликаты и проверить качество парсинга
"""

import sqlite3
import sys

DB_PATH = "nspd_lands.db"

def check_duplicates():
    """Проверка дубликатов в БД"""
    print("="*80)
    print("🔍 ПРОВЕРКА ДУБЛИКАТОВ В БД")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Получаем общую статистику
    cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
    unique_rows = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT page_number) FROM nspd_records")
    pages = cursor.fetchone()[0]
    
    print(f"\n📊 Общая статистика:")
    print(f"   Уникальных записей: {unique_rows:,}")
    print(f"   Страниц в БД: {pages:,}")
    
    # Проверяем дубликаты по первой колонке каждой записи
    # (предполагаем, что это кадастровый номер или ID)
    cursor.execute("""
        SELECT cell_value, COUNT(*) as cnt
        FROM nspd_records
        WHERE column_index = 0
        GROUP BY cell_value
        HAVING cnt > 1
        ORDER BY cnt DESC
        LIMIT 10
    """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n⚠️ Найдено дубликатов первой колонки: {len(duplicates)}")
        print("\nТоп-10 дублирующихся значений:")
        for value, count in duplicates:
            print(f"   '{value[:50]}...': {count} раз")
    else:
        print("\n✅ Дубликаты не найдены!")
    
    # Проверяем страницы с одинаковыми первыми записями
    cursor.execute("""
        SELECT 
            page_number,
            (SELECT cell_value 
             FROM nspd_records nr2 
             WHERE nr2.page_number = nr1.page_number 
               AND nr2.row_number_on_page = 1 
               AND nr2.column_index = 0
             LIMIT 1) as first_value
        FROM (SELECT DISTINCT page_number FROM nspd_records) nr1
        ORDER BY page_number
    """)
    
    page_first_values = cursor.fetchall()
    
    # Ищем повторяющиеся first_value
    from collections import Counter
    first_values_count = Counter([v for p, v in page_first_values if v])
    duplicated_first_values = {v: c for v, c in first_values_count.items() if c > 1}
    
    if duplicated_first_values:
        print(f"\n⚠️ Найдено страниц с одинаковыми первыми записями: {len(duplicated_first_values)}")
        print("\nПримеры:")
        for value, count in list(duplicated_first_values.items())[:5]:
            # Находим номера страниц с этим значением
            pages_with_value = [p for p, v in page_first_values if v == value]
            print(f"   '{value[:40]}...': страницы {pages_with_value[:5]}")
    else:
        print("\n✅ Все страницы имеют уникальные первые записи!")
    
    conn.close()
    
    print("\n" + "="*80)

if __name__ == "__main__":
    try:
        check_duplicates()
    except sqlite3.OperationalError as e:
        print(f"\n❌ Ошибка: База данных '{DB_PATH}' не найдена или повреждена")
        print(f"   Детали: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)







