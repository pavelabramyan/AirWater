#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ регионов и районов в базе данных
"""

import sqlite3
import re
from collections import defaultdict

db_path = 'land_records.db'

def extract_region_and_district(address):
    """Извлечение региона и района из адреса"""
    if not address:
        return None, None
    
    region = None
    district = None
    
    # Паттерны для регионов
    region_patterns = [
        r'([А-Яа-яЁё\s-]+?)\s+область',
        r'([А-Яа-яЁё\s-]+?)\s+обл\.',
        r'([А-Яа-яЁё\s-]+?)\s+край',
        r'([А-Яа-яЁё\s-]+?)\s+республика',
    ]
    
    for pattern in region_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            region = match.group(1).strip()
            break
    
    # Паттерны для районов
    district_patterns = [
        r'([А-Яа-яЁё\s-]+?)\s+муниципальный\s+(?:округ|район)',
        r'([А-Яа-яЁё\s-]+?)\s+(?:муниципальный\s+)?р-н',
        r'([А-Яа-яЁё\s-]+?)\s+район',
        r'город\s+([А-Яа-яЁё\s-]+)',
        r'г\.\s*([А-Яа-яЁё\s-]+)',
    ]
    
    for pattern in district_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            district = match.group(1).strip()
            break
    
    return region, district


def analyze_database():
    """Анализ базы данных по регионам и районам"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем все записи
    cursor.execute('SELECT cadastral_number, address, submission_status FROM land_records')
    records = cursor.fetchall()
    
    # Структура: {регион: {район: [список участков]}}
    regions_data = defaultdict(lambda: defaultdict(list))
    no_region = []
    
    print("🔍 Анализирую базу данных...\n")
    
    for cadastral, address, status in records:
        region, district = extract_region_and_district(address)
        
        if region:
            if not district:
                district = "Не определен"
            regions_data[region][district].append({
                'cadastral': cadastral,
                'address': address,
                'status': status or 'Не отправлена'
            })
        else:
            no_region.append({'cadastral': cadastral, 'address': address[:100] if address else 'Нет адреса'})
    
    # Выводим сводную таблицу
    print("=" * 100)
    print("СВОДНАЯ ТАБЛИЦА ПО РЕГИОНАМ И РАЙОНАМ")
    print("=" * 100)
    
    total_plots = 0
    
    for region in sorted(regions_data.keys()):
        districts = regions_data[region]
        region_total = sum(len(plots) for plots in districts.values())
        total_plots += region_total
        
        print(f"\n📍 {region.upper()}")
        print(f"   Всего участков: {region_total}")
        print(f"   Районов: {len(districts)}")
        print(f"\n   Районы:")
        
        for district in sorted(districts.keys()):
            plots = districts[district]
            submitted = sum(1 for p in plots if p['status'] and 'отправлена' in p['status'].lower())
            not_submitted = len(plots) - submitted
            
            print(f"      • {district}: {len(plots)} участков (отправлено: {submitted}, не отправлено: {not_submitted})")
    
    if no_region:
        print(f"\n⚠️  Участков без определенного региона: {len(no_region)}")
    
    print(f"\n" + "=" * 100)
    print(f"ИТОГО: {total_plots} участков в {len(regions_data)} регионах")
    print("=" * 100)
    
    # Детализация по Челябинской области
    print("\n\n" + "=" * 100)
    print("ДЕТАЛИЗАЦИЯ: ЧЕЛЯБИНСКАЯ ОБЛАСТЬ")
    print("=" * 100)
    
    chelyabinsk_found = False
    for region in regions_data.keys():
        if 'Челябинск' in region:
            chelyabinsk_found = True
            districts = regions_data[region]
            
            # Исключенные районы
            excluded = ['Сосновский', 'Аргаяшский', 'Еткульский', 'Челябинск']
            
            print(f"\n📊 Статистика по районам:")
            print(f"{'Район':<40} {'Всего':<10} {'Отправлено':<15} {'Осталось':<10} {'Статус'}")
            print("-" * 100)
            
            for district in sorted(districts.keys()):
                plots = districts[district]
                submitted = sum(1 for p in plots if p['status'] and 'отправлена' in p['status'].lower())
                not_submitted = len(plots) - submitted
                
                # Проверяем исключения
                is_excluded = any(excl in district for excl in excluded)
                status_text = "❌ Исключен" if is_excluded else ("✅ Готов" if not_submitted > 0 else "⏸️ Все отправлены")
                
                print(f"{district:<40} {len(plots):<10} {submitted:<15} {not_submitted:<10} {status_text}")
    
    if not chelyabinsk_found:
        print("⚠️  Челябинская область не найдена в базе данных")
    
    conn.close()
    
    return regions_data


if __name__ == "__main__":
    analyze_database()

