# Архитектура системы "Фабрика участков"

## Общая схема

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     CLI      │  │   Web App    │  │  REST API    │      │
│  │  (cli.py)    │  │ (web_app.py) │  │   (future)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬──────────────┬────────────────┬───────────────┘
             │              │                │
             ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         StorageService (storage_service.py)          │   │
│  │  • add_parcel()      • add_application()             │   │
│  │  • add_deal()        • get_analytics()               │   │
│  │  • Orchestrates business logic                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           │ uses protocols                   │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Ports (ports.py)                        │   │
│  │  • ParcelRepository (Protocol)                       │   │
│  │  • ApplicationRepository (Protocol)                  │   │
│  │  • DealRepository (Protocol)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────┬────────────────────────────────┬──────────────┘
              │                                │
              ▼                                ▼
┌─────────────────────────────────────────────────────────────┐
│                INFRASTRUCTURE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     SQLite Repositories (sqlite_repositories.py)     │   │
│  │  • SQLiteParcelRepository                            │   │
│  │  • SQLiteApplicationRepository                       │   │
│  │  • SQLiteDealRepository                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Database Layer (db.py)                     │   │
│  │  • init_database()                                   │   │
│  │  • get_connection()                                  │   │
│  │  • SQLite schema management                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   SQLite DB      │
                    │  parcels.db      │
                    └──────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Models (models.py)                      │   │
│  │                                                      │   │
│  │  @dataclass Parcel:                                  │   │
│  │    • cadastral_number, address, area                 │   │
│  │    • category, price, metadata                       │   │
│  │    • validate()                                      │   │
│  │                                                      │   │
│  │  @dataclass Application:                             │   │
│  │    • parcel_id, status, submitted_at                 │   │
│  │    • notes, can_submit()                             │   │
│  │                                                      │   │
│  │  @dataclass Deal:                                    │   │
│  │    • parcel_id, sale_price, buyer info               │   │
│  │    • status, mark_completed(), calculate_profit()    │   │
│  │                                                      │   │
│  │  Enums:                                              │   │
│  │    • LandCategory                                    │   │
│  │    • ApplicationStatus                               │   │
│  │    • DealStatus                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Принципы архитектуры

### 1. Чистая архитектура (Clean Architecture)

- **Domain Layer**: бизнес-логика и правила, не зависит ни от чего
- **Application Layer**: use-cases и оркестрация, зависит только от domain
- **Infrastructure Layer**: реализация портов, работа с БД и внешними сервисами
- **Interface Layer**: адаптеры для пользовательского взаимодействия

### 2. Dependency Inversion Principle (DIP)

- Application layer зависит от **интерфейсов** (Protocol), а не от конкретных реализаций
- Infrastructure layer **реализует** эти интерфейсы
- Легко заменить SQLite на PostgreSQL или любую другую БД

### 3. Single Responsibility Principle (SRP)

- Каждый модуль отвечает за одну вещь:
  - `models.py` — только доменные сущности
  - `storage_service.py` — только бизнес-операции
  - `sqlite_repositories.py` — только работа с БД

### 4. Open/Closed Principle (OCP)

- Система открыта для расширения, закрыта для модификации
- Новые функции добавляются через новые модули, не трогая существующий код

## Поток данных

### Добавление участка (пример)

```
1. User → CLI/Web Interface
   ├─ Ввод: cadastral_number, address, area, category, price
   │
2. Interface → StorageService.add_parcel()
   ├─ Создание доменной модели Parcel
   ├─ Валидация: parcel.validate()
   │
3. StorageService → ParcelRepository.add()
   ├─ Использование Protocol (абстракция)
   │
4. SQLiteParcelRepository → DB
   ├─ Конвертация Parcel → SQL INSERT
   ├─ Выполнение запроса в SQLite
   ├─ Получение generated ID
   │
5. Return flow: DB → Repository → Service → Interface → User
   └─ Возврат созданного Parcel с ID
```

### Получение аналитики (пример)

```
1. User → Interface (analytics page)
   │
2. Interface → StorageService.get_analytics()
   │
3. StorageService:
   ├─ parcels = ParcelRepository.list_all()
   ├─ applications = ApplicationRepository.list_all()
   ├─ deals = DealRepository.list_all()
   │
4. Business logic:
   ├─ Расчёт агрегатов (count, sum, average)
   ├─ Группировка по статусам
   ├─ Вычисление финансовых метрик
   │
5. Return: Dict[str, Any] с метриками
   │
6. Interface → Render analytics view
```

## Расширяемость

### Добавление нового интерфейса (например, Telegram Bot)

```python
# interface/telegram_bot.py
from application.storage_service import StorageService

class TelegramBot:
    def __init__(self, service: StorageService):
        self.service = service
    
    async def handle_add_parcel(self, message):
        parcel = self.service.add_parcel(...)
        await message.reply(f"Участок {parcel.id} добавлен!")
```

Не нужно менять domain, application или infrastructure!

### Добавление нового хранилища (например, PostgreSQL)

```python
# infrastructure/postgres_repositories.py
from application.ports import ParcelRepository
import asyncpg

class PostgresParcelRepository:
    def add(self, parcel: Parcel) -> Parcel:
        # Реализация для PostgreSQL
        ...
```

Просто заменяем репозиторий при инициализации — остальной код без изменений!

### Добавление нового use-case

```python
# application/scoring_service.py
from application.ports import ParcelRepository

class ScoringService:
    def __init__(self, parcel_repo: ParcelRepository):
        self.parcel_repo = parcel_repo
    
    def calculate_score(self, parcel_id: int) -> float:
        parcel = self.parcel_repo.get(parcel_id)
        # Бизнес-логика скоринга
        return score
```

Добавляем новый сервис без изменения существующих!

## Тестирование

### Изоляция слоёв

```python
# Тестирование domain layer (без БД)
def test_parcel_validation():
    parcel = Parcel(
        cadastral_number="123",
        area=-100,  # невалидная площадь
        ...
    )
    assert not parcel.validate()

# Тестирование application layer (с моками)
def test_storage_service_add_parcel(mock_repo):
    service = StorageService(mock_repo, ...)
    parcel = service.add_parcel(...)
    mock_repo.add.assert_called_once()

# Тестирование infrastructure layer (с тестовой БД)
def test_sqlite_repository(temp_db):
    repo = SQLiteParcelRepository(temp_db)
    parcel = repo.add(Parcel(...))
    assert parcel.id is not None
```

## Конфигурация и DI

```python
# main.py (пример точки входа)
import config
from infrastructure.db import init_database
from infrastructure.sqlite_repositories import *
from application.storage_service import StorageService

# 1. Инициализация инфраструктуры
init_database(config.DATABASE_PATH)

# 2. Создание репозиториев (конкретные реализации)
parcel_repo = SQLiteParcelRepository(config.DATABASE_PATH)
app_repo = SQLiteApplicationRepository(config.DATABASE_PATH)
deal_repo = SQLiteDealRepository(config.DATABASE_PATH)

# 3. Dependency Injection в сервис
service = StorageService(parcel_repo, app_repo, deal_repo)

# 4. Запуск интерфейса
app = create_web_app(service)
app.run()
```

## Best Practices

1. **Никогда не импортировать infrastructure в domain**
2. **Application зависит только от domain и портов**
3. **Infrastructure реализует порты**
4. **Interface использует application services**
5. **Все бизнес-правила только в domain/application**
6. **БД и внешние зависимости только в infrastructure**
7. **Логирование на всех уровнях кроме domain**
8. **Тесты для каждого слоя отдельно**

