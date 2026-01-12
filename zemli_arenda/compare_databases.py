#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сравнение двух баз данных: БД-1 (land_records.db) и БД-2 (nspd_lands.db)
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB1_PATH = "land_records.db"  # БД-1: Основная БД для отправки заявлений
DB2_PATH = "nspd_lands.db"    # БД-2: Новая БД из НСПД

def get_cadastral_numbers_from_db1():
    """
    Получить кадастровые номера из БД-1 (land_records.db)
    """
    logger.info("📊 Читаю кадастровые номера из БД-1 (land_records.db)...")
    
    conn = sqlite3.connect(DB1_PATH)
    cursor = conn.cursor()
    
    # Получаем все кадастровые номера
    cursor.execute("SELECT DISTINCT cadastral_number FROM land_records WHERE cadastral_number IS NOT NULL AND cadastral_number != ''")
    cadastral_numbers = set(row[0].strip() for row in cursor.fetchall())
    
    conn.close()
    
    logger.info(f"   Найдено уникальных кадастровых номеров: {len(cadastral_numbers)}")
    return cadastral_numbers

def get_cadastral_numbers_from_db2():
    """
    Получить кадастровые номера из БД-2 (nspd_lands.db)
    """
    logger.info("📊 Читаю кадастровые номера из БД-2 (nspd_lands.db)...")
    
    conn = sqlite3.connect(DB2_PATH)
    cursor = conn.cursor()
    
    # Получаем все кадастровые номера из колонки "Кадастровый номер/ Условный номер"
    cursor.execute("""
        SELECT DISTINCT cell_value 
        FROM nspd_records 
        WHERE column_name = 'Кадастровый номер/ Условный номер'
          AND cell_value IS NOT NULL 
          AND cell_value != ''
    """)
    cadastral_numbers = set(row[0].strip() for row in cursor.fetchall())
    
    conn.close()
    
    logger.info(f"   Найдено уникальных кадастровых номеров: {len(cadastral_numbers)}")
    return cadastral_numbers

def normalize_cadastral_number(cadastral):
    """
    Нормализация кадастрового номера (удаление пробелов, приведение к единому формату)
    """
    if not cadastral:
        return ""
    
    # Убираем пробелы, приводим к нижнему регистру
    normalized = cadastral.strip().replace(" ", "").lower()
    return normalized

def compare_databases():
    """
    Сравнить две базы данных
    """
    logger.info("="*80)
    logger.info("🔍 СРАВНЕНИЕ БАЗ ДАННЫХ")
    logger.info("="*80)
    logger.info("БД-1: land_records.db (основная БД для отправки заявлений)")
    logger.info("БД-2: nspd_lands.db (новая БД из НСПД)")
    logger.info("="*80)
    
    # Получаем кадастровые номера из обеих БД
    db1_cadastrals = get_cadastral_numbers_from_db1()
    db2_cadastrals = get_cadastral_numbers_from_db2()
    
    # Нормализуем кадастровые номера для точного сравнения
    logger.info("\n🔄 Нормализация кадастровых номеров...")
    db1_normalized = {normalize_cadastral_number(c): c for c in db1_cadastrals}
    db2_normalized = {normalize_cadastral_number(c): c for c in db2_cadastrals}
    
    # Сравниваем
    logger.info("\n📊 АНАЛИЗ...")
    
    # 1. Кадастровые номера, которые есть в БД-2, но нет в БД-1
    in_db2_not_in_db1 = set(db2_normalized.keys()) - set(db1_normalized.keys())
    
    # 2. Кадастровые номера, которые есть в БД-1, но нет в БД-2
    in_db1_not_in_db2 = set(db1_normalized.keys()) - set(db2_normalized.keys())
    
    # 3. Кадастровые номера, которые есть в обеих БД
    in_both = set(db1_normalized.keys()) & set(db2_normalized.keys())
    
    # Выводим результаты
    logger.info("\n" + "="*80)
    logger.info("📈 РЕЗУЛЬТАТЫ СРАВНЕНИЯ")
    logger.info("="*80)
    
    logger.info(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    logger.info(f"   БД-1 (land_records.db):  {len(db1_normalized):>8,} уникальных кадастровых номеров".replace(',', ' '))
    logger.info(f"   БД-2 (nspd_lands.db):    {len(db2_normalized):>8,} уникальных кадастровых номеров".replace(',', ' '))
    
    logger.info(f"\n🔍 ПЕРЕСЕЧЕНИЯ И РАЗЛИЧИЯ:")
    logger.info(f"   ✅ В обеих БД:           {len(in_both):>8,} кадастровых номеров".replace(',', ' '))
    logger.info(f"   ➕ Только в БД-2:        {len(in_db2_not_in_db1):>8,} кадастровых номеров (новые для нас)".replace(',', ' '))
    logger.info(f"   ➖ Только в БД-1:        {len(in_db1_not_in_db2):>8,} кадастровых номеров (отсутствуют в НСПД)".replace(',', ' '))
    
    # Вычисляем проценты
    if len(db1_normalized) > 0:
        overlap_percent_db1 = (len(in_both) / len(db1_normalized)) * 100
        logger.info(f"\n📊 ПРОЦЕНТНОЕ СООТНОШЕНИЕ:")
        logger.info(f"   Совпадение с БД-1: {overlap_percent_db1:.2f}%")
    
    if len(db2_normalized) > 0:
        overlap_percent_db2 = (len(in_both) / len(db2_normalized)) * 100
        logger.info(f"   Совпадение с БД-2: {overlap_percent_db2:.2f}%")
    
    # Примеры записей
    logger.info(f"\n📋 ПРИМЕРЫ КАДАСТРОВЫХ НОМЕРОВ:")
    
    if in_both:
        logger.info(f"\n   ✅ В ОБЕИХ БД (первые 5):")
        for i, cadastral_norm in enumerate(list(in_both)[:5], 1):
            logger.info(f"      {i}. {db1_normalized.get(cadastral_norm, db2_normalized.get(cadastral_norm))}")
    
    if in_db2_not_in_db1:
        logger.info(f"\n   ➕ ТОЛЬКО В БД-2 (первые 5 новых для нас):")
        for i, cadastral_norm in enumerate(list(in_db2_not_in_db1)[:5], 1):
            logger.info(f"      {i}. {db2_normalized[cadastral_norm]}")
    
    if in_db1_not_in_db2:
        logger.info(f"\n   ➖ ТОЛЬКО В БД-1 (первые 5, отсутствуют в НСПД):")
        for i, cadastral_norm in enumerate(list(in_db1_not_in_db2)[:5], 1):
            logger.info(f"      {i}. {db1_normalized[cadastral_norm]}")
    
    logger.info("\n" + "="*80)
    
    # Сохраняем результаты в файлы
    logger.info("\n💾 Сохранение результатов в файлы...")
    
    # Сохраняем список новых кадастровых номеров (только в БД-2)
    with open("new_cadastrals_in_nspd.txt", "w", encoding="utf-8") as f:
        f.write("# Кадастровые номера, которые есть в БД-2 (НСПД), но нет в БД-1\n")
        f.write(f"# Всего: {len(in_db2_not_in_db1)}\n\n")
        for cadastral_norm in sorted(in_db2_not_in_db1):
            f.write(f"{db2_normalized[cadastral_norm]}\n")
    
    logger.info(f"   ✅ Сохранено: new_cadastrals_in_nspd.txt ({len(in_db2_not_in_db1)} номеров)")
    
    # Сохраняем список кадастровых номеров, отсутствующих в НСПД (только в БД-1)
    with open("missing_in_nspd.txt", "w", encoding="utf-8") as f:
        f.write("# Кадастровые номера, которые есть в БД-1, но нет в БД-2 (НСПД)\n")
        f.write(f"# Всего: {len(in_db1_not_in_db2)}\n\n")
        for cadastral_norm in sorted(in_db1_not_in_db2):
            f.write(f"{db1_normalized[cadastral_norm]}\n")
    
    logger.info(f"   ✅ Сохранено: missing_in_nspd.txt ({len(in_db1_not_in_db2)} номеров)")
    
    # Сохраняем список общих кадастровых номеров
    with open("common_cadastrals.txt", "w", encoding="utf-8") as f:
        f.write("# Кадастровые номера, которые есть в обеих БД\n")
        f.write(f"# Всего: {len(in_both)}\n\n")
        for cadastral_norm in sorted(in_both):
            f.write(f"{db1_normalized[cadastral_norm]}\n")
    
    logger.info(f"   ✅ Сохранено: common_cadastrals.txt ({len(in_both)} номеров)")
    
    logger.info("\n" + "="*80)
    logger.info("✅ СРАВНЕНИЕ ЗАВЕРШЕНО!")
    logger.info("="*80)
    
    return {
        'db1_total': len(db1_normalized),
        'db2_total': len(db2_normalized),
        'in_both': len(in_both),
        'only_in_db2': len(in_db2_not_in_db1),
        'only_in_db1': len(in_db1_not_in_db2)
    }

def main():
    """Главная функция"""
    try:
        results = compare_databases()
        
        # Выводим финальную сводку
        print("\n" + "="*80)
        print("📊 ФИНАЛЬНАЯ СВОДКА")
        print("="*80)
        print(f"1️⃣  Кадастровых номеров в БД-2, но НЕТ в БД-1: {results['only_in_db2']:,}".replace(',', ' '))
        print(f"2️⃣  Кадастровых номеров в БД-1, но НЕТ в БД-2: {results['only_in_db1']:,}".replace(',', ' '))
        print(f"3️⃣  Кадастровых номеров в ОБЕИХ базах:       {results['in_both']:,}".replace(',', ' '))
        print("="*80)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при сравнении баз данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()







