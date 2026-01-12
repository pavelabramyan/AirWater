#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления дубликатов из БД nspd_lands.db
Безопасно работает параллельно с парсером
"""

import sqlite3
import shutil
import os
import sys
from datetime import datetime

DB_PATH = 'nspd_lands.db'
BACKUP_PATH = f'nspd_lands_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

def create_backup():
    """Создать резервную копию БД"""
    print("="*80)
    print("📦 СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ")
    print("="*80)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Файл {DB_PATH} не найден!")
        return False
    
    shutil.copy2(DB_PATH, BACKUP_PATH)
    backup_size = os.path.getsize(BACKUP_PATH) / (1024 * 1024)
    print(f"✅ Создана резервная копия: {BACKUP_PATH}")
    print(f"📊 Размер: {backup_size:.2f} MB")
    print()
    return True

def analyze_duplicates():
    """Анализ дубликатов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("="*80)
    print("🔍 АНАЛИЗ ДУБЛИКАТОВ")
    print("="*80)
    
    # Всего записей
    cursor.execute("SELECT COUNT(*) FROM nspd_records")
    total_records = cursor.fetchone()[0]
    
    # Всего участков
    cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
    total_parcels = cursor.fetchone()[0]
    
    # Уникальные кадастровые номера
    cursor.execute("""
        SELECT COUNT(DISTINCT cell_value) 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
    """)
    unique_cadastral = cursor.fetchone()[0]
    
    # Найти дубликаты
    cursor.execute("""
        SELECT cell_value, COUNT(*) as cnt
        FROM nspd_records
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
        GROUP BY cell_value
        HAVING cnt > 1
        ORDER BY cnt DESC
        LIMIT 10
    """)
    top_duplicates = cursor.fetchall()
    
    conn.close()
    
    print(f"📋 Всего ячеек: {total_records:,}")
    print(f"🏠 Всего участков: {total_parcels:,}")
    print(f"✅ Уникальных участков: {unique_cadastral:,}")
    print(f"🔴 Дубликатов: {total_parcels - unique_cadastral:,} ({((total_parcels - unique_cadastral) / total_parcels * 100):.1f}%)")
    print()
    print("🔝 ТОП-10 самых часто повторяющихся:")
    for i, (cadastral, count) in enumerate(top_duplicates, 1):
        print(f"   {i:2d}. {cadastral[:50]:50s} - {count:3d} раз")
    print()
    
    return total_parcels, unique_cadastral

def clean_duplicates(auto_confirm=False):
    """
    Удалить дубликаты, оставив только последние версии
    (по максимальному global_row_number для каждого кадастрового номера)
    """
    print("="*80)
    print("🧹 УДАЛЕНИЕ ДУБЛИКАТОВ")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Стратегия: оставляем записи с максимальным global_row_number для каждого кадастрового номера
    # Это значит оставляем самую последнюю спарсенную версию участка
    
    print("⏳ Шаг 1: Ищу дубликаты...")
    
    # Находим global_row_number для удаления
    cursor.execute("""
        WITH RankedRecords AS (
            SELECT 
                r1.global_row_number,
                r1.cell_value as cadastral,
                ROW_NUMBER() OVER (
                    PARTITION BY r1.cell_value 
                    ORDER BY r1.global_row_number DESC
                ) as rn
            FROM nspd_records r1
            WHERE r1.column_name = 'Кадастровый номер/ Условный номер'
            AND r1.cell_value != ''
        )
        SELECT global_row_number
        FROM RankedRecords
        WHERE rn > 1
    """)
    
    rows_to_delete = [row[0] for row in cursor.fetchall()]
    
    if not rows_to_delete:
        print("✅ Дубликатов не найдено!")
        conn.close()
        return
    
    print(f"📊 Найдено дубликатов: {len(rows_to_delete):,} участков")
    print()
    
    # Подсчитываем сколько ячеек удалим (порциями из-за ограничения SQLite)
    cells_to_delete = 0
    batch_size = 500
    
    for i in range(0, len(rows_to_delete), batch_size):
        batch = rows_to_delete[i:i+batch_size]
        placeholders = ','.join('?' * len(batch))
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM nspd_records
            WHERE global_row_number IN ({placeholders})
        """, batch)
        cells_to_delete += cursor.fetchone()[0]
    
    print(f"⚠️  Будет удалено:")
    print(f"   • {len(rows_to_delete):,} участков (строк)")
    print(f"   • {cells_to_delete:,} ячеек")
    print()
    
    # Подтверждение
    if not auto_confirm:
        confirm = input("👉 Продолжить удаление? (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y', 'да', 'д']:
            print("❌ Отменено пользователем")
            conn.close()
            return
    else:
        print("✅ Автоматическое подтверждение (--yes)")
    
    print()
    print("⏳ Шаг 2: Удаляю дубликаты...")
    
    # Удаляем порциями (SQLite ограничение на кол-во параметров)
    batch_size = 500
    deleted_total = 0
    
    for i in range(0, len(rows_to_delete), batch_size):
        batch = rows_to_delete[i:i+batch_size]
        placeholders = ','.join('?' * len(batch))
        
        cursor.execute(f"""
            DELETE FROM nspd_records
            WHERE global_row_number IN ({placeholders})
        """, batch)
        
        deleted_total += cursor.rowcount
        
        if (i // batch_size + 1) % 10 == 0:
            print(f"   Обработано: {i+len(batch):,}/{len(rows_to_delete):,} участков...")
    
    conn.commit()
    
    print(f"✅ Удалено {deleted_total:,} ячеек")
    print()
    
    # Вакуум для освобождения места
    print("⏳ Шаг 3: Оптимизирую БД (VACUUM)...")
    cursor.execute("VACUUM")
    
    conn.close()
    
    print("✅ Готово!")
    print()

def verify_cleanup():
    """Проверка результата"""
    print("="*80)
    print("✅ ПРОВЕРКА РЕЗУЛЬТАТА")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Всего записей после очистки
    cursor.execute("SELECT COUNT(*) FROM nspd_records")
    total_records = cursor.fetchone()[0]
    
    # Всего участков
    cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
    total_parcels = cursor.fetchone()[0]
    
    # Уникальные кадастровые номера
    cursor.execute("""
        SELECT COUNT(DISTINCT cell_value) 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
    """)
    unique_cadastral = cursor.fetchone()[0]
    
    # Размер БД
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)
    backup_size = os.path.getsize(BACKUP_PATH) / (1024 * 1024)
    
    conn.close()
    
    print(f"📋 Всего ячеек: {total_records:,}")
    print(f"🏠 Всего участков: {total_parcels:,}")
    print(f"✅ Уникальных участков: {unique_cadastral:,}")
    
    if total_parcels == unique_cadastral:
        print(f"🎉 УСПЕХ! Дубликаты удалены полностью!")
    else:
        print(f"⚠️  Осталось дубликатов: {total_parcels - unique_cadastral:,}")
    
    print()
    print(f"💾 Размер БД:")
    print(f"   До: {backup_size:.2f} MB")
    print(f"   После: {db_size:.2f} MB")
    print(f"   Экономия: {backup_size - db_size:.2f} MB ({((backup_size - db_size) / backup_size * 100):.1f}%)")
    print()

def main():
    print("\n" + "="*80)
    print("🧹 ОЧИСТКА ДУБЛИКАТОВ В БД nspd_lands.db")
    print("="*80)
    print()
    
    # Проверяем параметры командной строки
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    # Шаг 1: Резервная копия
    if not create_backup():
        return
    
    # Шаг 2: Анализ
    total_before, unique_before = analyze_duplicates()
    
    # Шаг 3: Очистка
    clean_duplicates(auto_confirm=auto_confirm)
    
    # Шаг 4: Проверка
    verify_cleanup()
    
    print("="*80)
    print(f"📦 Резервная копия сохранена: {BACKUP_PATH}")
    print("="*80)
    print()

if __name__ == '__main__':
    main()

