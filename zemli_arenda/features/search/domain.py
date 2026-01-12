"""
Доменные модели для модуля поиска участков
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class ParcelSource(str, Enum):
    """Источник данных об участке"""
    ROSREESTR_PKK = "Публичная кадастровая карта"
    ROSREESTR_API = "API Росреестра"
    MANUAL = "Ручной ввод"
    IMPORT_FILE = "Импорт из файла"


class ParcelAvailability(str, Enum):
    """Доступность участка для получения"""
    FREE = "Свободен"  # Нет правообладателей
    STATE_OWNERSHIP = "Госсобственность не разграничена"
    HAS_OWNER = "Есть правообладатель"
    ENCUMBERED = "Есть обременения"
    UNKNOWN = "Неизвестно"


@dataclass
class SearchCriteria:
    """Критерии поиска участков"""
    region_code: str  # Код региона (74 для Челябинска)
    min_area: Optional[float] = None  # Минимальная площадь в кв.м
    max_area: Optional[float] = None  # Максимальная площадь в кв.м
    categories: Optional[List[str]] = None  # Категории земли
    max_distance_km: Optional[float] = None  # Макс расстояние от города
    only_free: bool = True  # Только свободные участки
    bbox: Optional[Dict[str, float]] = None  # Границы поиска (lat/lon)
    
    def validate(self) -> bool:
        """Валидация критериев"""
        if self.min_area and self.max_area and self.min_area > self.max_area:
            return False
        if not self.region_code:
            return False
        return True


@dataclass
class FoundParcel:
    """Найденный участок (кандидат для добавления)"""
    cadastral_number: str
    address: str
    area: float
    category: str
    source: ParcelSource
    availability: ParcelAvailability
    
    # Дополнительная информация
    district: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None  # {"lat": ..., "lon": ...}
    estimated_price: Optional[float] = None
    has_encumbrances: bool = False
    has_owner: bool = False
    purpose: Optional[str] = None  # Разрешённое использование
    
    # Метаданные поиска
    found_at: datetime = field(default_factory=datetime.now)
    raw_data: Optional[Dict[str, Any]] = None
    
    def is_suitable(self) -> bool:
        """Проверка, подходит ли участок для НСПД"""
        # Участок должен быть свободным или госсобственность
        if self.availability not in [ParcelAvailability.FREE, ParcelAvailability.STATE_OWNERSHIP]:
            return False
        
        # Не должно быть обременений
        if self.has_encumbrances:
            return False
        
        # Категории, подходящие для НСПД
        suitable_categories = ["ИЖС", "ЛПХ", "Садоводство", "Огородничество"]
        if self.category not in suitable_categories:
            return False
        
        return True
    
    def calculate_priority_score(self) -> float:
        """Расчёт приоритета участка (чем выше, тем лучше)"""
        score = 100.0
        
        # Доступность
        if self.availability == ParcelAvailability.FREE:
            score += 50
        elif self.availability == ParcelAvailability.STATE_OWNERSHIP:
            score += 30
        
        # Категория
        if self.category == "ИЖС":
            score += 30
        elif self.category == "ЛПХ":
            score += 20
        
        # Площадь (оптимально 800-1500 кв.м)
        if 800 <= self.area <= 1500:
            score += 20
        elif 600 <= self.area <= 2000:
            score += 10
        
        # Наличие координат
        if self.coordinates:
            score += 10
        
        # Адрес
        if self.address and len(self.address) > 10:
            score += 5
        
        return score


@dataclass
class SearchResult:
    """Результат поиска"""
    criteria: SearchCriteria
    found_parcels: List[FoundParcel]
    total_found: int
    filtered_count: int  # Сколько подходящих после фильтрации
    search_started_at: datetime
    search_completed_at: datetime
    errors: List[str] = field(default_factory=list)
    
    @property
    def duration_seconds(self) -> float:
        """Длительность поиска в секундах"""
        delta = self.search_completed_at - self.search_started_at
        return delta.total_seconds()
    
    def get_top_parcels(self, limit: int = 10) -> List[FoundParcel]:
        """Получить топ участков по приоритету"""
        suitable = [p for p in self.found_parcels if p.is_suitable()]
        sorted_parcels = sorted(suitable, key=lambda p: p.calculate_priority_score(), reverse=True)
        return sorted_parcels[:limit]















