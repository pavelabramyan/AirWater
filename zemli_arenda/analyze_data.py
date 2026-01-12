#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
from collections import defaultdict

# Читаем CSV
df = pd.read_csv('land_records_20251117_003657.csv')

print(f"Всего участков в БД: {len(df)}\n")
print("=" * 100)

# Функция для извлечения региона и района из адреса
def parse_address(address):
    if pd.isna(address):
        return ("Неизвестно", "Неизвестно")
    
    address = str(address)
    
    # Паттерны для регионов
    # Ищем область, край, республику и т.д.
    region_patterns = [
        r'([А-ЯЁа-яё\s-]+(?:область|обл\.?))',
        r'([А-ЯЁа-яё\s-]+(?:край))',
        r'([А-ЯЁа-яё\s-]+(?:Республика))',
        r'([А-ЯЁа-яё\s-]+(?:автономный округ|АО))',
    ]
    
    region = "Неизвестно"
    for pattern in region_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            region = match.group(1).strip()
            # Убираем лишние пробелы и "обл."
            region = re.sub(r'\s+', ' ', region)
            region = re.sub(r'\s*обл\.?\s*$', ' область', region).strip()
            break
    
    # Паттерны для районов
    district_patterns = [
        r'([А-ЯЁа-яё\s-]+(?:муниципальный округ|м\.?\s?о\.?))',
        r'([А-ЯЁа-яё\s-]+(?:муниципальный район|м\.?\s?р-н\.?))',
        r'([А-ЯЁа-яё\s-]+(?:район|р-н\.?))',
        r'([А-ЯЁа-яё\s-]+(?:городской округ|г\.?\s?о\.?))',
        r'город\s+([А-ЯЁа-яё]+)',
        r'г\.\s*([А-ЯЁа-яё]+)',
    ]
    
    district = "Неизвестно"
    for pattern in district_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            district = match.group(1).strip()
            # Убираем лишние пробелы
            district = re.sub(r'\s+', ' ', district)
            # Убираем "р-н", "муниципальный округ" из конца
            district = re.sub(r'\s*(р-н\.?|район|муниципальный округ|муниципальный район|м\.?\s?о\.?|м\.?\s?р-н\.?)$', '', district, flags=re.IGNORECASE).strip()
            break
    
    return (region, district)

# Парсим все адреса
df[['регион', 'район']] = df['адрес'].apply(lambda x: pd.Series(parse_address(x)))

# Создаем сводную таблицу
summary = df.groupby(['регион', 'район']).size().reset_index(name='количество участков')
summary = summary.sort_values(['регион', 'количество участков'], ascending=[True, False])

print("\n📊 СВОДНАЯ ТАБЛИЦА ПО РЕГИОНАМ И РАЙОНАМ:\n")
print("=" * 100)

current_region = None
region_total = 0
grand_total = 0

for _, row in summary.iterrows():
    region = row['регион']
    district = row['район']
    count = row['количество участков']
    
    if current_region != region:
        if current_region is not None:
            print(f"{'└─ ИТОГО по региону ' + current_region + ':':.<80} {region_total:>6} участков")
            print("=" * 100)
        current_region = region
        region_total = 0
        print(f"\n🌍 {region.upper()}")
        print("-" * 100)
    
    print(f"   ├─ {district:<70} {count:>6} участков")
    region_total += count
    grand_total += count

if current_region is not None:
    print(f"{'└─ ИТОГО по региону ' + current_region + ':':.<80} {region_total:>6} участков")
    print("=" * 100)

print(f"\n{'🌟 ВСЕГО УЧАСТКОВ В БАЗЕ:':.<80} {grand_total:>6}")
print("=" * 100)

# Отдельно выводим регионы с количеством районов
print("\n\n📍 СПИСОК РЕГИОНОВ:\n")
print("=" * 100)
regions_summary = summary.groupby('регион').agg({
    'район': 'count',
    'количество участков': 'sum'
}).reset_index()
regions_summary.columns = ['Регион', 'Количество районов', 'Всего участков']
regions_summary = regions_summary.sort_values('Всего участков', ascending=False)

for _, row in regions_summary.iterrows():
    print(f"{row['Регион']:<60} | Районов: {row['Количество районов']:>3} | Участков: {row['Всего участков']:>6}")

print("=" * 100)

# Фильтруем Челябинскую область
chelyabinsk = summary[summary['регион'].str.contains('Челябинск', case=False, na=False)]
if not chelyabinsk.empty:
    print("\n\n🎯 ЧЕЛЯБИНСКАЯ ОБЛАСТЬ (стартовый регион):\n")
    print("=" * 100)
    excluded_districts = ['Сосновский', 'Аргаяшский', 'Еткульский', 'Челябинск']
    
    for _, row in chelyabinsk.iterrows():
        district = row['район']
        count = row['количество участков']
        
        # Проверяем, не входит ли район в исключения
        is_excluded = any(excl.lower() in district.lower() for excl in excluded_districts)
        status = " ⚠️  (УЖЕ ОТПРАВЛЕНЫ)" if is_excluded else " ✅ (ДОСТУПНО - отправить 10 заявок)"
        
        print(f"   {district:<60} {count:>6} участков {status}")
    
    print("=" * 100)

# Сохраняем детальную таблицу в CSV
summary.to_csv('regions_districts_summary.csv', index=False, encoding='utf-8-sig')
print("\n✅ Сводная таблица сохранена в: regions_districts_summary.csv")

# Сохраняем список регионов
regions_summary.to_csv('regions_summary.csv', index=False, encoding='utf-8-sig')
print("✅ Список регионов сохранен в: regions_summary.csv")


