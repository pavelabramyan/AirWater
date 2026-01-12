#!/usr/bin/env python3
"""
Скрипт для автоматического определения названий районов
по кадастровым номерам через поиск в интернете
"""

import sqlite3
from collections import defaultdict
import time

DB_PATH = 'land_records.db'

def get_unique_cadastral_quarters():
    """Извлечь все уникальные кадастровые кварталы (регион:район) из БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT cadastral_number 
        FROM land_records 
        WHERE cadastral_number IS NOT NULL AND cadastral_number != ''
    """)
    
    cadastrals = cursor.fetchall()
    conn.close()
    
    # Извлекаем уникальные кварталы (первые 2 части)
    quarters = set()
    for (cad,) in cadastrals:
        parts = cad.strip().split(':')
        if len(parts) >= 2:
            region = parts[0].strip()
            district = parts[1].strip()
            # Пропускаем некорректные (с пробелами внутри номера)
            if ' ' not in region and ' ' not in district:
                quarters.add(f"{region}:{district}")
    
    return sorted(quarters)

def main():
    print("=" * 80)
    print("🔍 АНАЛИЗ КАДАСТРОВЫХ КВАРТАЛОВ В БД")
    print("=" * 80)
    
    quarters = get_unique_cadastral_quarters()
    
    print(f"\n📊 Найдено уникальных кадастровых кварталов: {len(quarters)}")
    
    # Группируем по регионам
    by_region = defaultdict(list)
    for q in quarters:
        region = q.split(':')[0]
        by_region[region].append(q)
    
    print(f"📍 Количество регионов: {len(by_region)}")
    print("\n" + "-" * 80)
    print("СТАТИСТИКА ПО РЕГИОНАМ:")
    print("-" * 80)
    
    for region in sorted(by_region.keys(), key=lambda x: int(x) if x.isdigit() else 999):
        districts = by_region[region]
        print(f"Регион {region}: {len(districts)} районов")
    
    # Сохраняем список для ручного поиска
    with open('cadastral_quarters_to_search.txt', 'w', encoding='utf-8') as f:
        f.write("# Список кадастровых кварталов для поиска названий районов\n")
        f.write("# Формат: регион:район\n\n")
        for region in sorted(by_region.keys(), key=lambda x: int(x) if x.isdigit() else 999):
            f.write(f"\n# === РЕГИОН {region} ===\n")
            for q in sorted(by_region[region]):
                f.write(f"{q}\n")
    
    print("\n" + "=" * 80)
    print("✅ Список сохранён в файл: cadastral_quarters_to_search.txt")
    print("=" * 80)
    print(f"\nВсего нужно найти названия для {len(quarters)} кадастровых кварталов")

if __name__ == '__main__':
    main()

