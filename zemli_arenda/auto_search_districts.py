#!/usr/bin/env python3
"""
Автоматический поиск названий районов по кадастровым кварталам
через веб-поиск
"""

import sqlite3
import json
import time
from collections import defaultdict

DB_PATH = 'land_records.db'
CACHE_FILE = 'district_cache.json'

# Загружаем существующий справочник
try:
    from fill_districts_full import REGION_DISTRICTS
    print(f"✅ Загружен базовый справочник: {len(REGION_DISTRICTS)} регионов")
    district_cache = dict(REGION_DISTRICTS)
except:
    district_cache = {}
    print("⚠️  Базовый справочник не найден, начинаю с нуля")

# Пробуем загрузить кэш
try:
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cached = json.load(f)
        for region, districts in cached.items():
            if region not in district_cache:
                district_cache[region] = {}
            district_cache[region].update(districts)
        print(f"✅ Загружен кэш: дополнительно {sum(len(d) for d in cached.values())} районов")
except:
    print("⚠️  Кэш не найден")

def get_unique_quarters_with_counts():
    """Получить уникальные кварталы с количеством записей"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cadastral_number, COUNT(*) as cnt
        FROM land_records 
        WHERE cadastral_number IS NOT NULL AND cadastral_number != ''
        GROUP BY SUBSTR(cadastral_number, 1, INSTR(cadastral_number || ':', ':', INSTR(cadastral_number, ':')+1)-1)
    """)
    
    quarters = defaultdict(int)
    for cad, cnt in cursor.fetchall():
        parts = cad.strip().split(':')
        if len(parts) >= 2:
            region = parts[0].strip()
            district = parts[1].strip()
            if ' ' not in region and ' ' not in district and region.isdigit():
                key = f"{region}:{district}"
                quarters[key] += cnt
    
    conn.close()
    return quarters

def search_district_name(region_code, district_code):
    """
    Поиск названия района по коду.
    Пока возвращает None - будет дополнено веб-поиском
    """
    # Проверяем кэш
    if region_code in district_cache:
        if district_code in district_cache[region_code]:
            return district_cache[region_code][district_code]
    
    # TODO: Здесь будет веб-поиск
    # Пока возвращаем None
    return None

def save_cache():
    """Сохранить текущий справочник в кэш"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(district_cache, f, ensure_ascii=False, indent=2)
    print(f"💾 Кэш сохранён: {sum(len(d) for d in district_cache.values())} районов")

def main():
    print("\n" + "=" * 80)
    print("🔍 АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ НАЗВАНИЙ РАЙОНОВ")
    print("=" * 80)
    
    quarters = get_unique_quarters_with_counts()
    
    print(f"\n📊 Всего уникальных кварталов: {len(quarters)}")
    
    # Сортируем по количеству записей (самые популярные первыми)
    sorted_quarters = sorted(quarters.items(), key=lambda x: x[1], reverse=True)
    
    found = 0
    not_found = 0
    
    print("\n🔄 Проверяю наличие в справочнике...\n")
    
    missing = []
    
    for quarter, count in sorted_quarters:
        region, district = quarter.split(':')
        name = search_district_name(region, district)
        
        if name:
            found += 1
        else:
            not_found += 1
            missing.append((quarter, count))
    
    print(f"✅ Найдено в справочнике: {found}")
    print(f"❌ Отсутствует: {not_found}")
    
    if missing:
        print("\n" + "-" * 80)
        print("📋 ТОП-50 ОТСУТСТВУЮЩИХ КВАРТАЛОВ (по количеству записей):")
        print("-" * 80)
        print(f"{'Квартал':<15} {'Записей':<10} {'Нужно найти'}")
        print("-" * 80)
        
        for quarter, count in missing[:50]:
            region, district = quarter.split(':')
            print(f"{quarter:<15} {count:<10} Регион {region}, район {district}")
    
    print("\n" + "=" * 80)
    print("📝 СЛЕДУЮЩИЕ ШАГИ:")
    print("=" * 80)
    print("1. Для автоматического поиска нужно добавить веб-поиск API")
    print("2. ИЛИ можно заполнить вручную самые популярные районы")
    print(f"3. Всего отсутствует: {not_found} кварталов")
    
    save_cache()

if __name__ == '__main__':
    main()

