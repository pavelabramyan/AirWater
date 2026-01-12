#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПРАВИЛЬНЫЙ скрипт для удаления дубликатов
Удаляет дубликаты по кадастровому номеру, оставляя последнюю версию
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
    
    # Всего уникальных кадастров
    cursor.execute("""
        SELECT COUNT(DISTINCT cell_value) 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
    """)
    unique_cadastral = cursor.fetchone()[0]
    
    # Всего записей с кадастром
    cursor.execute("""
        SELECT COUNT(*) 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
    """)
    total_cadastral = cursor.fetchone()[0]
    
    # Всего участков (по global_row_number)
    cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
    total_parcels = cursor.fetchone()[0]
    
    duplicates = total_cadastral - unique_cadastral
    
    print(f"🏠 Уникальных кадастровых номеров: {unique_cadastral:,}")
    print(f"📋 Всего записей с кадастром: {total_cadastral:,}")
    print(f"📊 Всего участков (global_row_number): {total_parcels:,}")
    print(f"🔴 Дубликатов: {duplicates:,} ({(duplicates / total_cadastral * 100):.1f}%)")
    print()
    
    conn.close()
    
    return unique_cadastral, total_cadastral

def clean_duplicates_correct(auto_confirm=False):
    """
    ПРАВИЛЬНОЕ удаление дубликатов
    Для каждого кадастрового номера оставляем только записи с максимальным global_row_number
    """
    print("="*80)
    print("🧹 УДАЛЕНИЕ ДУБЛИКАТОВ (ПРАВИЛЬНЫЙ МЕТОД)")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("⏳ Шаг 1: Находим ID записей для удаления...")
    print("   Стратегия: для каждого кадастра оставляем только записи с MAX(global_row_number)")
    print()
    
    # Находим ID всех записей, которые НЕ имеют максимальный global_row_number для своего кадастра
    cursor.execute("""
        WITH MaxGlobalRows AS (
            SELECT 
                cell_value as cadastral,
                MAX(global_row_number) as max_global_row
            FROM nspd_records
            WHERE column_name = 'Кадастровый номер/ Условный номер'
            AND cell_value != ''
            GROUP BY cell_value
            HAVING COUNT(*) > 1
        )
        SELECT r.id
        FROM nspd_records r
        INNER JOIN MaxGlobalRows m ON (
            r.cell_value = m.cadastral 
            AND r.column_name = 'Кадастровый номер/ Условный номер'
            AND r.global_row_number < m.max_global_row
        )
    """)
    
    ids_to_delete = [row[0] for row in cursor.fetchall()]
    
    if not ids_to_delete:
        print("✅ Дубликатов не найдено!")
        conn.close()
        return
    
    print(f"📊 Найдено записей для удаления: {len(ids_to_delete):,}")
    print()
    
    # Подсчитываем сколько участков (global_row_number) удалим
    batch_size = 500
    unique_global_rows_to_delete = set()
    
    for i in range(0, len(ids_to_delete), batch_size):
        batch = ids_to_delete[i:i+batch_size]
        placeholders = ','.join('?' * len(batch))
        cursor.execute(f"""
            SELECT DISTINCT global_row_number
            FROM nspd_records
            WHERE id IN ({placeholders})
        """, batch)
        unique_global_rows_to_delete.update([row[0] for row in cursor.fetchall()])
    
    print(f"⚠️  Будет удалено:")
    print(f"   • {len(unique_global_rows_to_delete):,} участков (строк)")
    print(f"   • {len(ids_to_delete):,} ячеек")
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
    
    # Удаляем порциями
    deleted_total = 0
    
    for i in range(0, len(ids_to_delete), batch_size):
        batch = ids_to_delete[i:i+batch_size]
        placeholders = ','.join('?' * len(batch))
        
        cursor.execute(f"""
            DELETE FROM nspd_records
            WHERE id IN ({placeholders})
        """, batch)
        
        deleted_total += cursor.rowcount
        
        if (i // batch_size + 1) % 10 == 0:
            print(f"   Обработано: {i+len(batch):,}/{len(ids_to_delete):,} записей...")
    
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
    
    # Всего записей с кадастром
    cursor.execute("""
        SELECT COUNT(*) 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
        AND cell_value != ''
    """)
    total_cadastral_records = cursor.fetchone()[0]
    
    # Размер БД
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)
    backup_size = os.path.getsize(BACKUP_PATH) / (1024 * 1024)
    
    conn.close()
    
    print(f"📋 Всего ячеек: {total_records:,}")
    print(f"🏠 Всего участков: {total_parcels:,}")
    print(f"✅ Уникальных кадастров: {unique_cadastral:,}")
    print(f"📊 Записей с кадастром: {total_cadastral_records:,}")
    print()
    
    if unique_cadastral == total_cadastral_records:
        print(f"🎉 УСПЕХ! Дубликаты удалены полностью!")
    else:
        duplicates = total_cadastral_records - unique_cadastral
        print(f"⚠️  Осталось дубликатов: {duplicates:,} ({(duplicates / total_cadastral_records * 100):.1f}%)")
    
    print()
    print(f"💾 Размер БД:")
    print(f"   До: {backup_size:.2f} MB")
    print(f"   После: {db_size:.2f} MB")
    print(f"   Экономия: {backup_size - db_size:.2f} MB ({((backup_size - db_size) / backup_size * 100):.1f}%)")
    print()

def main():
    print("\n" + "="*80)
    print("🧹 ПРАВИЛЬНАЯ ОЧИСТКА ДУБЛИКАТОВ В БД nspd_lands.db")
    print("="*80)
    print()
    
    # Проверяем параметры командной строки
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    # Шаг 1: Резервная копия
    if not create_backup():
        return
    
    # Шаг 2: Анализ
    unique_before, total_before = analyze_duplicates()
    
    # Шаг 3: Очистка
    clean_duplicates_correct(auto_confirm=auto_confirm)
    
    # Шаг 4: Проверка
    verify_cleanup()
    
    print("="*80)
    print(f"📦 Резервная копия сохранена: {BACKUP_PATH}")
    print("="*80)
    print()

if __name__ == '__main__':
    main()







