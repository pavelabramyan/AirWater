# 🚀 Быстрый старт: Фабрика участков

## Установка (30 секунд)

```bash
# 1. Перейти в директорию проекта
cd Земли

# 2. Создать виртуальное окружение
python3 -m venv .venv

# 3. Активировать
source .venv/bin/activate  # Mac/Linux
# или
.venv\Scripts\activate  # Windows

# 4. Установить зависимости
pip install -r requirements.txt
```

## Быстрая демонстрация

```bash
python demo.py
```

Результат: система создаст 3 участка, 3 заявки, 2 сделки и покажет полную аналитику.

## CLI интерфейс

```bash
python run_cli.py
```

**Что можно делать:**
1. Добавить участок → ввести данные → готово
2. Список участков → увидеть все участки
3. Добавить заявку → выбрать участок → указать статус
4. Аналитика → посмотреть статистику

## Веб-интерфейс

```bash
python run_web.py
```

Откройте в браузере: **http://127.0.0.1:8080**

**Страницы:**
- `/` — Главная (дашборд со статистикой)
- `/parcels` — Список участков
- `/parcels/add` — Добавить участок
- `/applications` — Список заявок
- `/applications/add` — Создать заявку
- `/deals` — Список сделок
- `/deals/add` — Добавить сделку
- `/analytics` — Детальная аналитика

## Примеры использования

### Python API

```python
from domain.models import LandCategory, ApplicationStatus, DealStatus
from application.storage_service import StorageService
from infrastructure.db import init_database
from infrastructure.sqlite_repositories import *
import config

# Инициализация
init_database(config.DATABASE_PATH)
service = StorageService(
    SQLiteParcelRepository(config.DATABASE_PATH),
    SQLiteApplicationRepository(config.DATABASE_PATH),
    SQLiteDealRepository(config.DATABASE_PATH)
)

# Добавить участок
parcel = service.add_parcel(
    cadastral_number="74:36:0123456:100",
    address="г. Челябинск, ул. Ленина, 1",
    area=1000.0,
    category=LandCategory.IZhS,
    price=50000.0
)
print(f"Участок добавлен с ID: {parcel.id}")

# Создать заявку
app = service.add_application(
    parcel_id=parcel.id,
    status=ApplicationStatus.SUBMITTED,
    notes="Заявка подана через МФЦ"
)
print(f"Заявка создана: #{app.id}")

# Зарегистрировать сделку
deal = service.add_deal(
    parcel_id=parcel.id,
    sale_price=450000.0,
    buyer_name="Иванов Иван",
    buyer_contact="+7 900 123-45-67",
    status=DealStatus.COMPLETED
)
print(f"Сделка завершена: {deal.sale_price:,.0f} руб")

# Получить аналитику
analytics = service.get_analytics()
print(f"Всего участков: {analytics['total_parcels']}")
print(f"Общая выручка: {analytics['total_revenue']:,.0f} руб")
```

## Тестирование

```bash
# Запустить все тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=domain --cov=application --cov=infrastructure -v
```

## Конфигурация

Файл `config.py`:

```python
# Путь к БД
DATABASE_PATH = "data/parcels.db"

# Логирование
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"

# Веб-сервер
WEB_HOST = "127.0.0.1"
WEB_PORT = 8080
```

## Структура БД

```sql
-- Участки
CREATE TABLE parcels (
    id INTEGER PRIMARY KEY,
    cadastral_number TEXT UNIQUE,
    address TEXT,
    area REAL,
    category TEXT,
    price REAL,
    metadata TEXT,  -- JSON
    created_at TEXT
);

-- Заявки
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    parcel_id INTEGER,
    status TEXT,
    submitted_at TEXT,
    notes TEXT,
    FOREIGN KEY (parcel_id) REFERENCES parcels(id)
);

-- Сделки
CREATE TABLE deals (
    id INTEGER PRIMARY KEY,
    parcel_id INTEGER,
    sale_price REAL,
    buyer_name TEXT,
    buyer_contact TEXT,
    status TEXT,
    created_at TEXT,
    completed_at TEXT,
    FOREIGN KEY (parcel_id) REFERENCES parcels(id)
);
```

## Частые задачи

### Добавить участок через Web

1. Запустить `python run_web.py`
2. Открыть http://127.0.0.1:8080
3. Нажать "Добавить участок"
4. Заполнить форму
5. Нажать "Добавить"

### Посмотреть статистику

**CLI:**
```bash
python run_cli.py
# Выбрать пункт "7. Аналитика"
```

**Web:**
```
http://127.0.0.1:8080/analytics
```

**Python:**
```python
analytics = service.get_analytics()
print(analytics)
```

### Экспортировать данные

```python
import json

# Получить все участки
parcels = service.get_all_parcels()

# Конвертировать в dict
parcels_dict = [
    {
        'id': p.id,
        'cadastral_number': p.cadastral_number,
        'address': p.address,
        'area': p.area,
        'category': p.category.value,
        'price': p.price
    }
    for p in parcels
]

# Сохранить в JSON
with open('parcels_export.json', 'w', encoding='utf-8') as f:
    json.dump(parcels_dict, f, ensure_ascii=False, indent=2)
```

## Решение проблем

### Ошибка: "ModuleNotFoundError"
```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate

# Переустановите зависимости
pip install -r requirements.txt
```

### Ошибка: "Database is locked"
```bash
# Закройте все другие подключения к БД
# Перезапустите приложение
```

### Веб-интерфейс не открывается
```bash
# Проверьте, что порт 8080 свободен
lsof -i :8080

# Или измените порт в config.py
WEB_PORT = 8081
```

## Полезные команды

```bash
# Очистить БД
rm -rf data/

# Очистить логи
rm -rf logs/

# Запустить с отладкой
python run_web.py  # Flask debug mode включён по умолчанию

# Проверить структуру БД
sqlite3 data/parcels.db ".schema"

# Посмотреть данные
sqlite3 data/parcels.db "SELECT * FROM parcels;"
```

## Дальше

- Подробная документация: `README.md`
- Архитектура системы: `ARCHITECTURE.md`
- История изменений: `CHANGELOG.md`
- Полный отчёт: `ОТЧЕТ_ЭТАП1.md`

---

**Вопросы?** Читайте документацию или экспериментируйте с кодом!

