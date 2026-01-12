#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Экспорт данных из БД НСПД в CSV
"""

import sqlite3
import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = "nspd_lands.db"

def export_to_csv(output_file="nspd_export.csv"):
    """
    Экспорт данных из БД в CSV файл
    
    Args:
        output_file: Путь к выходному CSV файлу
    """
    logger.info("="*80)
    logger.info("📤 ЭКСПОРТ ДАННЫХ ИЗ БД В CSV")
    logger.info("="*80)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем наличие данных
        cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
        total_rows = cursor.fetchone()[0]
        
        if total_rows == 0:
            logger.error("❌ База данных пуста!")
            return
        
        logger.info(f"📊 Найдено записей: {total_rows}")
        
        # Получаем уникальные номера записей
        cursor.execute('SELECT DISTINCT global_row_number FROM nspd_records ORDER BY global_row_number')
        row_numbers = [r[0] for r in cursor.fetchall()]
        
        logger.info(f"📝 Начинаю экспорт в {output_file}...")
        
        # Экспортируем в CSV
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')  # Используем ; для совместимости с Excel
            
            headers_written = False
            
            for idx, row_num in enumerate(row_numbers, 1):
                # Получаем данные строки
                cursor.execute('''
                    SELECT column_name, cell_value 
                    FROM nspd_records 
                    WHERE global_row_number = ? 
                    ORDER BY column_index
                ''', (row_num,))
                
                data = cursor.fetchall()
                
                if not data:
                    continue
                
                # Записываем заголовки (только один раз)
                if not headers_written:
                    headers = [d[0] for d in data]
                    writer.writerow(headers)
                    headers_written = True
                    logger.info(f"   Колонок: {len(headers)}")
                    logger.info(f"   Заголовки: {headers[:5]}{'...' if len(headers) > 5 else ''}")
                
                # Записываем данные
                values = [d[1] for d in data]
                writer.writerow(values)
                
                # Прогресс каждые 1000 записей
                if idx % 1000 == 0:
                    progress = (idx / total_rows) * 100
                    logger.info(f"   📊 Прогресс: {idx}/{total_rows} ({progress:.1f}%)")
        
        conn.close()
        
        logger.info("\n" + "="*80)
        logger.info("✅ ЭКСПОРТ ЗАВЕРШЁН!")
        logger.info("="*80)
        logger.info(f"📁 Файл: {output_file}")
        logger.info(f"📊 Экспортировано записей: {total_rows}")
        logger.info("="*80)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при экспорте: {e}")
        import traceback
        traceback.print_exc()

def show_statistics():
    """Показать статистику по БД"""
    logger.info("="*80)
    logger.info("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
    logger.info("="*80)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Общее количество записей
        cursor.execute("SELECT COUNT(DISTINCT global_row_number) FROM nspd_records")
        total_records = cursor.fetchone()[0]
        logger.info(f"📋 Всего записей: {total_records}")
        
        # Количество колонок
        cursor.execute("SELECT COUNT(DISTINCT column_name) FROM nspd_records")
        total_columns = cursor.fetchone()[0]
        logger.info(f"📊 Количество колонок: {total_columns}")
        
        # Список колонок
        cursor.execute("""
            SELECT DISTINCT column_name 
            FROM nspd_records 
            WHERE global_row_number = 1 
            ORDER BY column_index
        """)
        columns = [r[0] for r in cursor.fetchall()]
        logger.info(f"📝 Колонки: {', '.join(columns)}")
        
        # Прогресс парсинга
        cursor.execute("SELECT * FROM parsing_metadata WHERE id=1")
        metadata = cursor.fetchone()
        
        if metadata:
            logger.info(f"\n📈 Прогресс парсинга:")
            logger.info(f"   Всего страниц: {metadata[1]}")
            logger.info(f"   Всего записей: {metadata[2]}")
            logger.info(f"   Спарсено страниц: {metadata[3]}")
            logger.info(f"   Спарсено записей: {metadata[4]}")
            logger.info(f"   Последняя страница: {metadata[5]}")
            logger.info(f"   Начато: {metadata[6]}")
            logger.info(f"   Обновлено: {metadata[7]}")
            
            if metadata[2] > 0:
                progress = (metadata[4] / metadata[2]) * 100
                logger.info(f"   Прогресс: {progress:.2f}%")
        
        # Примеры данных
        logger.info(f"\n📄 Примеры данных (первые 3 записи):")
        for row_num in range(1, min(4, total_records + 1)):
            cursor.execute("""
                SELECT column_name, cell_value 
                FROM nspd_records 
                WHERE global_row_number = ? 
                ORDER BY column_index
                LIMIT 3
            """, (row_num,))
            
            data = cursor.fetchall()
            logger.info(f"\n   Запись #{row_num}:")
            for col_name, col_value in data:
                logger.info(f"      {col_name}: {col_value[:50]}{'...' if len(col_value) > 50 else ''}")
        
        conn.close()
        logger.info("\n" + "="*80)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при получении статистики: {e}")

def main():
    """Главная функция"""
    print("\n" + "="*80)
    print("📤 ЭКСПОРТ ДАННЫХ НСПД")
    print("="*80)
    print("1. Показать статистику БД")
    print("2. Экспортировать в CSV")
    print("3. Выход")
    print("="*80)
    
    choice = input("\n👉 Ваш выбор: ").strip()
    
    if choice == "1":
        show_statistics()
    elif choice == "2":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"nspd_export_{timestamp}.csv"
        export_to_csv(output_file)
    elif choice == "3":
        logger.info("👋 До свидания!")
    else:
        logger.error("❌ Неверный выбор!")

if __name__ == "__main__":
    main()







