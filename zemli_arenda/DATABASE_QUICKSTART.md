# 🗄️ База данных земельных участков - Быстрый старт

## ✅ Что готово

- ✅ **База данных SQLite**: `land_records.db` (53 МБ, 74,748 записей)
- ✅ **CSV файл**: `land_records_20251117_003657.csv` (25 МБ)
- ✅ **Python API**: Класс `LandRecordsDB` для работы с БД
- ✅ **Интерактивная программа**: `interactive_search.py`

## 🚀 Быстрый старт

### 1. Интерактивный поиск

```bash
python3 interactive_search.py
```

Появится меню с опциями:
1. Поиск по региону
2. Поиск по виду использования
3. Поиск по площади
4. Поиск по кадастровому номеру
5. Статистика

### 2. Использование в своем скрипте

```python
from land_db import LandRecordsDB

# Вариант 1: Контекстный менеджер (рекомендуется)
with LandRecordsDB() as db:
    # Поиск по адресу
    results = db.search_by_address("Московская область", limit=10)
    for record in results:
        print(f"{record['cadastral_number']}: {record['address']}")

# Вариант 2: Расширенный поиск с фильтрами
with LandRecordsDB() as db:
    results = db.advanced_search(
        address="Тамбовская область",
        permitted_use="индивидуального жилищного",
        min_area=1000,
        max_area=3000,
        limit=20
    )
```

### 3. Прямая работа с SQLite

```python
import sqlite3

conn = sqlite3.connect('land_records.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT cadastral_number, address, area 
    FROM land_records 
    WHERE land_category = 'Земли населенных пунктов'
    LIMIT 10
''')

for row in cursor.fetchall():
    print(row)

conn.close()
```

## 📊 Структура таблицы

```sql
CREATE TABLE land_records (
    id INTEGER PRIMARY KEY,
    cadastral_number TEXT,    -- Кадастровый номер
    address TEXT,             -- Адрес
    land_category TEXT,       -- Категория земель
    permitted_use TEXT,       -- Вид использования
    area TEXT,                -- Площадь (м²)
    plot_type TEXT,           -- Тип участка
    created_at TIMESTAMP      -- Время добавления
)
```

## 🔍 Основные методы LandRecordsDB

| Метод | Описание | Пример |
|-------|----------|--------|
| `search_by_cadastral_number()` | Поиск по кадастровому номеру | `db.search_by_cadastral_number("68:06:0801001:ЗУ4")` |
| `search_by_address()` | Поиск по адресу | `db.search_by_address("Москва", limit=100)` |
| `search_by_category()` | Поиск по категории | `db.search_by_category("Земли населенных пунктов")` |
| `search_by_plot_type()` | Поиск по типу | `db.search_by_plot_type("Земельный участок")` |
| `search_by_permitted_use()` | Поиск по использованию | `db.search_by_permitted_use("индивидуального жилищного")` |
| `advanced_search()` | Расширенный поиск | См. примеры ниже |
| `get_statistics()` | Статистика | `db.get_statistics()` |

## 💡 Примеры запросов

### Пример 1: Все участки для ИЖС в регионе

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.advanced_search(
        address="Тамбовская область",
        permitted_use="индивидуального жилищного строительства",
        limit=50
    )
    
    print(f"Найдено: {len(results)} участков")
```

### Пример 2: Участки определенной площади

```python
with LandRecordsDB() as db:
    results = db.advanced_search(
        land_category="Земли населенных пунктов",
        min_area=1500,
        max_area=2500,
        limit=30
    )
```

### Пример 3: Экспорт в CSV

```python
import pandas as pd
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.search_by_address("Санкт-Петербург", limit=1000)
    df = pd.DataFrame(results)
    df.to_csv('filtered_plots.csv', index=False, encoding='utf-8-sig')
```

### Пример 4: Статистика по региону

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.search_by_address("Московская область", limit=10000)
    
    # Группировка по типу
    by_type = {}
    for record in results:
        plot_type = record['plot_type']
        by_type[plot_type] = by_type.get(plot_type, 0) + 1
    
    for plot_type, count in by_type.items():
        print(f"{plot_type}: {count}")
```

## 📚 Полная документация

Смотрите `README_DATABASE.md` для подробной документации:
- Все методы API
- Примеры использования
- SQL запросы
- Создание веб-API
- Устранение проблем

## 🔧 Пересоздание базы данных

Если нужно пересоздать базу из CSV:

```bash
python3 create_database.py
```

## 📁 Файлы проекта

```
land_records.db              # База данных (53 МБ)
land_records_*.csv           # CSV файлы
land_db.py                   # Класс для работы с БД
interactive_search.py        # Интерактивный поиск
create_database.py          # Создание БД из CSV
README_DATABASE.md          # Полная документация
```

## 💬 Примеры вывода

### Поиск по региону:
```
✅ Найдено 100 участков (показаны первые 10):

1. Кадастровый номер: 68:06:0801001:ЗУ4
   Адрес: Тамбовская область, муниципальный округ Кирсановский...
   Категория: Земли населенных пунктов
   Площадь: 5053 м²
   Тип: Территория
```

### Статистика:
```
📊 Общая статистика:
   Всего записей в базе: 74,748

📋 Распределение по категориям земель:
   • Земли населенных пунктов: 70,498 (94.3%)
   • Земли сельскохозяйственного назначения: 498 (0.7%)

🏗️  Распределение по типам участков:
   • Земельный участок: 64,491 (86.3%)
   • Территория: 10,257 (13.7%)
```

## ⚡ Производительность

- Поиск по индексу (кадастровый номер): < 1 мс
- Поиск по адресу (LIKE): 10-50 мс
- Расширенный поиск: 20-100 мс
- Полная таблица (74K записей): ~200 мс

Индексы оптимизированы для быстрого поиска! 🚀


