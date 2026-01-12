# 🎉 База данных земельных участков - ГОТОВА!

## ✅ Что создано

### 1. База данных SQLite
- **Файл**: `land_records.db` (53 МБ)
- **Записей**: 74,748
- **Таблица**: `land_records` с 8 колонками
- **Индексы**: 4 индекса для быстрого поиска

### 2. Исходные данные
- **CSV файл**: `land_records_20251117_003657.csv` (25 МБ)
- **Источник**: API сайта nspd.gov.ru
- **Колонки**: 
  - кадастровый номер
  - адрес
  - категория земель
  - вид разрешенного использования
  - площадь
  - тип участка

### 3. Python модули

#### `land_db.py` - Класс для работы с БД
```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.search_by_address("Москва", limit=10)
```

**Методы:**
- `search_by_cadastral_number()` - поиск по кадастровому номеру
- `search_by_address()` - поиск по адресу
- `search_by_category()` - поиск по категории земель
- `search_by_plot_type()` - поиск по типу участка
- `search_by_permitted_use()` - поиск по виду использования
- `advanced_search()` - расширенный поиск с множественными фильтрами
- `get_statistics()` - статистика по БД
- `get_all_categories()` - список всех категорий
- `get_all_plot_types()` - список всех типов

#### `create_database.py` - Создание БД из CSV
```bash
python3 create_database.py
```
Автоматически находит последний CSV файл и создает базу данных.

#### `interactive_search.py` - Интерактивная программа
```bash
python3 interactive_search.py
```
Меню с опциями поиска:
1. Поиск по региону
2. Поиск по виду использования  
3. Поиск по площади
4. Поиск по кадастровому номеру
5. Статистика

#### `scraper_api.py` - Извлечение данных с API
```bash
python3 scraper_api.py
```
Извлекает данные напрямую с API сайта (748 страниц × 100 записей).

### 4. Документация

- **`DATABASE_QUICKSTART.md`** - Быстрый старт (краткая инструкция)
- **`README_DATABASE.md`** - Полная документация с примерами
- **`README.md`** - Общее описание проекта

## 🚀 Как использовать

### Вариант 1: Интерактивный поиск

```bash
python3 interactive_search.py
```

### Вариант 2: В своем скрипте

```python
from land_db import LandRecordsDB

# Простой поиск
with LandRecordsDB() as db:
    # По адресу
    results = db.search_by_address("Тамбовская область", limit=10)
    
    # По кадастровому номеру
    record = db.search_by_cadastral_number("68:06:0801001:ЗУ4")
    
    # Расширенный поиск
    results = db.advanced_search(
        address="Москва",
        permitted_use="индивидуального жилищного",
        min_area=1000,
        max_area=3000,
        limit=20
    )
    
    # Статистика
    stats = db.get_statistics()
    print(f"Всего записей: {stats['total_records']}")
```

### Вариант 3: Прямой SQL

```python
import sqlite3

conn = sqlite3.connect('land_records.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT cadastral_number, address, area 
    FROM land_records 
    WHERE land_category = 'Земли населенных пунктов'
    AND CAST(REPLACE(area, ' ', '') AS INTEGER) BETWEEN 1000 AND 3000
    LIMIT 10
''')

for row in cursor.fetchall():
    print(row)

conn.close()
```

## 📊 Статистика базы данных

```
Всего записей: 74,748

По категориям:
  • Земли населенных пунктов: 70,498 (94.3%)
  • Земли сельскохозяйственного назначения: 498 (0.7%)
  • Прочие: 3,752 (5.0%)

По типам:
  • Земельный участок: 64,491 (86.3%)
  • Территория: 10,257 (13.7%)

По регионам:
  • Тамбовская область: ~74,000+
  • Московская область: 86
  • И другие регионы
```

## ⚡ Производительность

- **Размер БД**: 53 МБ
- **Поиск по индексу**: < 1 мс
- **Поиск по адресу**: 10-50 мс
- **Расширенный поиск**: 20-100 мс
- **Полная статистика**: ~200 мс

## 📁 Структура файлов

```
Земли/
├── land_records.db                  # База данных (53 МБ) ⭐
├── land_records_20251117_003657.csv # CSV файл (25 МБ)
├── land_db.py                       # Класс для работы с БД ⭐
├── interactive_search.py            # Интерактивная программа ⭐
├── create_database.py               # Создание БД из CSV
├── scraper_api.py                   # Извлечение данных с API
├── DATABASE_QUICKSTART.md           # Быстрый старт ⭐
├── README_DATABASE.md               # Полная документация
└── requirements.txt                 # Зависимости
```

## 💡 Примеры использования

### Пример 1: Найти участки для ИЖС

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.advanced_search(
        address="Тамбовская область",
        permitted_use="индивидуального жилищного строительства",
        min_area=800,
        max_area=2000,
        limit=50
    )
    
    print(f"Найдено {len(results)} участков для ИЖС")
    
    for record in results:
        print(f"• {record['cadastral_number']}")
        print(f"  Адрес: {record['address'][:60]}...")
        print(f"  Площадь: {record['area']} м²")
        print()
```

### Пример 2: Экспорт в новый CSV

```python
from land_db import LandRecordsDB
import pandas as pd

with LandRecordsDB() as db:
    # Все участки в определенном регионе
    results = db.search_by_address("Московская область", limit=1000)
    
    # Конвертируем в DataFrame
    df = pd.DataFrame(results)
    
    # Сохраняем
    df.to_csv('moscow_region_plots.csv', index=False, encoding='utf-8-sig')
    
    print(f"Экспортировано {len(df)} записей")
```

### Пример 3: Статистика по региону

```python
from land_db import LandRecordsDB
from collections import Counter

with LandRecordsDB() as db:
    results = db.search_by_address("Тамбовская область", limit=10000)
    
    # Статистика по использованию
    uses = Counter(r['permitted_use'] for r in results)
    
    print("Топ-5 видов использования:")
    for use, count in uses.most_common(5):
        print(f"  {use[:60]}: {count}")
```

## 🔄 Обновление данных

Чтобы обновить данные из API:

```bash
# 1. Извлечь свежие данные (займет ~15 минут)
python3 scraper_api.py

# 2. Пересоздать базу данных
python3 create_database.py
```

## 🎯 Следующие шаги

База данных готова для использования в ваших скриптах! Вы можете:

1. **Интегрировать** класс `LandRecordsDB` в существующий проект
2. **Создать веб-API** (см. пример в `README_DATABASE.md`)
3. **Добавить дополнительные фильтры** в методы поиска
4. **Реализовать автоматическое обновление** данных
5. **Создать веб-интерфейс** для поиска участков

## 📞 Справка

- **Быстрый старт**: `DATABASE_QUICKSTART.md`
- **Полная документация**: `README_DATABASE.md`
- **Примеры**: `land_db.py` (в конце файла функция `main()`)
- **Интерактивная программа**: `python3 interactive_search.py`

---

**Создано**: 2025-11-17  
**Записей в БД**: 74,748  
**Размер БД**: 53 МБ  
**Статус**: ✅ Готово к использованию


