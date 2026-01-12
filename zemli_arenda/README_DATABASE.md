# База данных земельных участков

## 📊 Обзор

База данных SQLite содержит **74,748 записей** о свободных земельных участках или территориях, находящихся в государственной или муниципальной собственности.

**Файл БД**: `land_records.db` (53 МБ)

## 🗂️ Структура таблицы

### Таблица `land_records`

| Колонка | Тип | Описание | Индекс |
|---------|-----|----------|--------|
| `id` | INTEGER | Уникальный идентификатор (PRIMARY KEY) | ✓ |
| `cadastral_number` | TEXT | Кадастровый номер участка | ✓ |
| `address` | TEXT | Адрес/описание местоположения | ✓ |
| `land_category` | TEXT | Категория земель | ✓ |
| `permitted_use` | TEXT | Вид разрешенного использования | |
| `area` | TEXT | Площадь (м²) | |
| `plot_type` | TEXT | Тип участка | ✓ |
| `created_at` | TIMESTAMP | Время добавления в БД | |

## 📈 Статистика

- **Всего записей**: 74,748
- **Категории земель**: 8 уникальных
- **Типы участков**: 2 (Земельный участок, Территория)

### Распределение по категориям:
- Земли населенных пунктов: 70,498 (94.3%)
- Земли сельскохозяйственного назначения: 498 (0.7%)
- Земли населённых пунктов: 241 (0.3%)
- Прочие: 3,511 (4.7%)

### Распределение по типам:
- Земельный участок: 64,491 (86.3%)
- Территория: 10,257 (13.7%)

## 🚀 Быстрый старт

### Создание базы данных из CSV

```bash
python3 create_database.py
```

Скрипт автоматически найдет последний CSV файл и создаст базу данных.

### Использование класса LandRecordsDB

```python
from land_db import LandRecordsDB

# Вариант 1: С контекстным менеджером (рекомендуется)
with LandRecordsDB() as db:
    # Поиск по кадастровому номеру
    record = db.search_by_cadastral_number("68:06:0801001:ЗУ4")
    print(record)

# Вариант 2: Явное управление соединением
db = LandRecordsDB()
db.connect()
results = db.search_by_address("Москва")
db.close()
```

## 📚 API класса LandRecordsDB

### Основные методы поиска

#### 1. Поиск по кадастровому номеру

```python
record = db.search_by_cadastral_number("68:06:0801001:ЗУ4")
# Возвращает: Dict или None
```

**Пример результата:**
```python
{
    'id': 1,
    'cadastral_number': '68:06:0801001:ЗУ4',
    'address': 'Тамбовская область, муниципальный округ Кирсановский...',
    'land_category': 'Земли населенных пунктов',
    'permitted_use': 'Для ведения личного подсобного хозяйства...',
    'area': '5053',
    'plot_type': 'Территория',
    'created_at': '2025-11-17 00:40:40'
}
```

#### 2. Поиск по адресу

```python
results = db.search_by_address("Московская область", limit=100)
# Возвращает: List[Dict]
```

Поддерживает частичное совпадение (LIKE).

#### 3. Поиск по категории земель

```python
results = db.search_by_category("Земли населенных пунктов", limit=100)
# Возвращает: List[Dict]
```

#### 4. Поиск по типу участка

```python
results = db.search_by_plot_type("Земельный участок", limit=100)
# Возвращает: List[Dict]
```

Доступные типы:
- `"Земельный участок"`
- `"Территория"`

#### 5. Поиск по виду разрешенного использования

```python
results = db.search_by_permitted_use("индивидуального жилищного", limit=100)
# Возвращает: List[Dict]
```

Поддерживает частичное совпадение (LIKE).

### Расширенный поиск

#### 6. Поиск с множественными фильтрами

```python
results = db.advanced_search(
    address="Москва",
    land_category="Земли населенных пунктов",
    plot_type="Земельный участок",
    permitted_use="индивидуального жилищного",
    min_area=1000,  # минимальная площадь в м²
    max_area=5000,  # максимальная площадь в м²
    limit=50
)
# Возвращает: List[Dict]
```

**Параметры:**
- `address` (str, optional): Часть адреса
- `land_category` (str, optional): Точная категория земель
- `plot_type` (str, optional): Тип участка
- `permitted_use` (str, optional): Часть описания использования
- `min_area` (float, optional): Минимальная площадь (м²)
- `max_area` (float, optional): Максимальная площадь (м²)
- `limit` (int, default=100): Максимальное количество результатов

### Статистика и справочники

#### 7. Получение статистики

```python
stats = db.get_statistics()
# Возвращает: Dict
```

**Структура результата:**
```python
{
    'total_records': 74748,
    'by_category': {
        'Земли населенных пунктов': 70498,
        'Земли сельскохозяйственного назначения': 498,
        ...
    },
    'by_type': {
        'Земельный участок': 64491,
        'Территория': 10257
    }
}
```

#### 8. Получение списка категорий

```python
categories = db.get_all_categories()
# Возвращает: List[str]
```

#### 9. Получение списка типов участков

```python
types = db.get_all_plot_types()
# Возвращает: List[str]
```

## 💡 Примеры использования

### Пример 1: Найти все участки в Тамбовской области для ИЖС

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    results = db.advanced_search(
        address="Тамбовская область",
        permitted_use="индивидуального жилищного строительства",
        limit=10
    )
    
    print(f"Найдено: {len(results)} участков\n")
    
    for record in results:
        print(f"Кадастровый номер: {record['cadastral_number']}")
        print(f"Адрес: {record['address']}")
        print(f"Площадь: {record['area']} м²")
        print("-" * 80)
```

### Пример 2: Статистика по региону

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    # Все участки в Московской области
    results = db.search_by_address("Московская область", limit=10000)
    
    print(f"Всего участков в Московской области: {len(results)}")
    
    # Группировка по типу
    by_type = {}
    for record in results:
        plot_type = record['plot_type']
        by_type[plot_type] = by_type.get(plot_type, 0) + 1
    
    print("\nПо типам:")
    for plot_type, count in by_type.items():
        print(f"  {plot_type}: {count}")
```

### Пример 3: Поиск участков определенной площади

```python
from land_db import LandRecordsDB

with LandRecordsDB() as db:
    # Участки площадью от 1000 до 2000 м²
    results = db.advanced_search(
        land_category="Земли населенных пунктов",
        min_area=1000,
        max_area=2000,
        limit=20
    )
    
    for record in results:
        print(f"{record['cadastral_number']}: {record['area']} м²")
```

### Пример 4: Экспорт результатов поиска

```python
from land_db import LandRecordsDB
import pandas as pd

with LandRecordsDB() as db:
    results = db.search_by_address("Санкт-Петербург", limit=1000)
    
    # Конвертируем в DataFrame
    df = pd.DataFrame(results)
    
    # Сохраняем в новый CSV
    df.to_csv('spb_plots.csv', index=False, encoding='utf-8-sig')
    
    print(f"Экспортировано {len(df)} записей в spb_plots.csv")
```

### Пример 5: Создание веб-API (FastAPI)

```python
from fastapi import FastAPI, Query
from land_db import LandRecordsDB
from typing import Optional, List

app = FastAPI()

@app.get("/api/search")
def search_plots(
    address: Optional[str] = None,
    category: Optional[str] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    limit: int = Query(default=100, le=1000)
):
    with LandRecordsDB() as db:
        results = db.advanced_search(
            address=address,
            land_category=category,
            min_area=min_area,
            max_area=max_area,
            limit=limit
        )
        return {"count": len(results), "results": results}

@app.get("/api/statistics")
def get_stats():
    with LandRecordsDB() as db:
        return db.get_statistics()

# Запуск: uvicorn your_file:app --reload
```

## 🔧 Прямые SQL запросы

Если нужны более сложные запросы, можно работать напрямую с SQLite:

```python
import sqlite3

conn = sqlite3.connect('land_records.db')
cursor = conn.cursor()

# Пример: Топ-10 самых больших участков
cursor.execute('''
    SELECT cadastral_number, address, area, plot_type
    FROM land_records
    WHERE area IS NOT NULL
    ORDER BY CAST(REPLACE(area, ' ', '') AS INTEGER) DESC
    LIMIT 10
''')

for row in cursor.fetchall():
    print(row)

conn.close()
```

## 📁 Файлы проекта

```
Земли/
├── land_records.db              # База данных SQLite (53 МБ)
├── land_records_*.csv           # Исходные CSV файлы
├── create_database.py           # Скрипт создания БД из CSV
├── land_db.py                   # Класс для работы с БД
├── scraper_api.py              # Скрипт извлечения данных с API
├── README_DATABASE.md          # Эта документация
└── requirements.txt            # Зависимости
```

## 🔍 Индексы для быстрого поиска

База данных оптимизирована с помощью индексов:

- `idx_cadastral_number` - для поиска по кадастровому номеру
- `idx_land_category` - для фильтрации по категории
- `idx_plot_type` - для фильтрации по типу участка
- `idx_address` - для поиска по адресу

Это обеспечивает быстрый поиск даже по большому объему данных.

## ⚠️ Важные замечания

1. **Площадь**: Хранится как текст, может содержать пробелы. При фильтрации по площади используйте `CAST(REPLACE(area, ' ', '') AS INTEGER)`.

2. **NULL значения**: Некоторые записи могут иметь `None` в категории земель (3,450 записей).

3. **Кодировка**: Все данные в UTF-8. CSV файлы сохраняются с BOM для корректного открытия в Excel.

4. **Производительность**: Для больших выборок (>10,000 записей) используйте индексы и ограничивайте результаты с помощью `LIMIT`.

## 🆘 Устранение проблем

### База данных не найдена

```bash
# Создайте заново
python3 create_database.py
```

### Медленные запросы

- Проверьте наличие индексов: `PRAGMA index_list('land_records');`
- Используйте `EXPLAIN QUERY PLAN` для анализа
- Ограничивайте результаты с помощью `LIMIT`

### Ошибки кодировки

```python
# При чтении используйте правильную кодировку
conn = sqlite3.connect('land_records.db')
conn.text_factory = str  # Для Python 3
```

## 📞 Поддержка

Если возникли вопросы по работе с базой данных:
1. Проверьте примеры в `land_db.py`
2. Запустите тесты: `python3 land_db.py`
3. Просмотрите логи создания БД в консоли

---

**Версия**: 1.0  
**Дата**: 2025-11-17  
**Записей**: 74,748


