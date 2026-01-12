#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания базы данных SQLite из CSV файла с земельными участками
"""

import sqlite3
import pandas as pd
import logging
from datetime import datetime
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_database(csv_file, db_file='land_records.db'):
    """
    Создание базы данных SQLite из CSV файла
    
    Args:
        csv_file: Путь к CSV файлу
        db_file: Имя файла базы данных (по умолчанию land_records.db)
    """
    try:
        logger.info(f"Чтение CSV файла: {csv_file}")
        
        # Проверяем существование файла
        if not os.path.exists(csv_file):
            logger.error(f"Файл {csv_file} не найден")
            return False
        
        # Читаем CSV
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        logger.info(f"Загружено {len(df)} записей из CSV")
        logger.info(f"Колонки: {', '.join(df.columns)}")
        
        # Удаляем старую базу данных если существует
        if os.path.exists(db_file):
            os.remove(db_file)
            logger.info(f"Удалена старая база данных: {db_file}")
        
        # Создаем подключение к базе данных
        logger.info(f"Создание базы данных: {db_file}")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Создаем таблицу с индексами
        logger.info("Создание таблицы land_records...")
        cursor.execute('''
            CREATE TABLE land_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cadastral_number TEXT NOT NULL,
                address TEXT,
                land_category TEXT,
                permitted_use TEXT,
                area TEXT,
                plot_type TEXT,
                cadastral_cost REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем индексы для быстрого поиска
        logger.info("Создание индексов...")
        cursor.execute('CREATE INDEX idx_cadastral_number ON land_records(cadastral_number)')
        cursor.execute('CREATE INDEX idx_land_category ON land_records(land_category)')
        cursor.execute('CREATE INDEX idx_plot_type ON land_records(plot_type)')
        cursor.execute('CREATE INDEX idx_address ON land_records(address)')
        
        # Вставляем данные
        logger.info("Загрузка данных в базу...")
        insert_count = 0
        
        for index, row in df.iterrows():
            cursor.execute('''
                INSERT INTO land_records 
                (cadastral_number, address, land_category, permitted_use, area, plot_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row.get('кадастровый номер', ''),
                row.get('адрес', ''),
                row.get('категория земель', ''),
                row.get('вид разрешенного использования', ''),
                row.get('площадь', ''),
                row.get('тип участка', '')
            ))
            
            insert_count += 1
            
            # Показываем прогресс каждые 1000 записей
            if insert_count % 1000 == 0:
                logger.info(f"Загружено {insert_count}/{len(df)} записей...")
        
        # Сохраняем изменения
        conn.commit()
        logger.info(f"Все {insert_count} записей успешно загружены в базу данных")
        
        # Статистика
        cursor.execute('SELECT COUNT(*) FROM land_records')
        total_records = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT land_category) FROM land_records')
        unique_categories = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT plot_type) FROM land_records')
        unique_types = cursor.fetchone()[0]
        
        logger.info("\n=== СТАТИСТИКА БАЗЫ ДАННЫХ ===")
        logger.info(f"Всего записей: {total_records}")
        logger.info(f"Уникальных категорий земель: {unique_categories}")
        logger.info(f"Уникальных типов участков: {unique_types}")
        
        # Показываем примеры категорий
        cursor.execute('SELECT land_category, COUNT(*) as cnt FROM land_records GROUP BY land_category ORDER BY cnt DESC LIMIT 5')
        logger.info("\nТоп-5 категорий земель:")
        for category, count in cursor.fetchall():
            logger.info(f"  - {category}: {count} записей")
        
        # Показываем размер базы данных
        db_size = os.path.getsize(db_file) / (1024 * 1024)  # в МБ
        logger.info(f"\nРазмер базы данных: {db_size:.2f} МБ")
        
        conn.close()
        logger.info(f"\n✅ База данных успешно создана: {db_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}", exc_info=True)
        return False


def test_database(db_file='land_records.db'):
    """
    Тестирование базы данных - примеры запросов
    
    Args:
        db_file: Имя файла базы данных
    """
    try:
        logger.info("\n=== ТЕСТИРОВАНИЕ БАЗЫ ДАННЫХ ===")
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Пример 1: Поиск по кадастровому номеру
        logger.info("\n1. Поиск по кадастровому номеру (первые 3 записи):")
        cursor.execute('SELECT * FROM land_records LIMIT 3')
        for row in cursor.fetchall():
            logger.info(f"  ID: {row[0]}, Кадастровый номер: {row[1]}, Адрес: {row[2][:50]}...")
        
        # Пример 2: Поиск по категории
        logger.info("\n2. Подсчет по категориям земель:")
        cursor.execute('''
            SELECT land_category, COUNT(*) as count 
            FROM land_records 
            GROUP BY land_category 
            ORDER BY count DESC
        ''')
        for category, count in cursor.fetchall():
            logger.info(f"  {category}: {count} участков")
        
        # Пример 3: Поиск по типу участка
        logger.info("\n3. Подсчет по типам участков:")
        cursor.execute('''
            SELECT plot_type, COUNT(*) as count 
            FROM land_records 
            GROUP BY plot_type 
            ORDER BY count DESC
        ''')
        for plot_type, count in cursor.fetchall():
            logger.info(f"  {plot_type}: {count} участков")
        
        # Пример 4: Поиск по адресу (содержит "Москва")
        logger.info("\n4. Поиск участков в Московской области:")
        cursor.execute('''
            SELECT COUNT(*) 
            FROM land_records 
            WHERE address LIKE '%Московская область%'
        ''')
        moscow_count = cursor.fetchone()[0]
        logger.info(f"  Найдено: {moscow_count} участков")
        
        conn.close()
        logger.info("\n✅ Тестирование завершено успешно")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании базы данных: {e}", exc_info=True)
        return False


def main():
    """Главная функция"""
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info("СОЗДАНИЕ БАЗЫ ДАННЫХ ИЗ CSV")
    logger.info(f"Время старта: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # Ищем последний созданный CSV файл
    import glob
    csv_files = glob.glob('land_records_*.csv')
    
    if not csv_files:
        logger.error("CSV файлы не найдены. Сначала запустите scraper_api.py")
        return
    
    # Берем самый последний файл
    csv_file = max(csv_files, key=os.path.getctime)
    logger.info(f"Используется CSV файл: {csv_file}")
    
    # Создаем базу данных
    db_file = 'land_records.db'
    if create_database(csv_file, db_file):
        # Тестируем базу данных
        test_database(db_file)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("\n" + "=" * 80)
        logger.info("БАЗА ДАННЫХ ГОТОВА К ИСПОЛЬЗОВАНИЮ")
        logger.info(f"Время окончания: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Длительность: {duration}")
        logger.info(f"Файл базы данных: {db_file}")
        logger.info("=" * 80)
    else:
        logger.error("Не удалось создать базу данных")


if __name__ == "__main__":
    main()


