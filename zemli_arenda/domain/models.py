"""
Доменные модели системы "Фабрика участков"
Чистая бизнес-логика без зависимостей от инфраструктуры
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class LandCategory(str, Enum):
    """Категория земли"""
    IZhS = "ИЖС"  # Индивидуальное жилищное строительство
    LPKh = "ЛПХ"  # Личное подсобное хозяйство
    COMMERCE = "Коммерческая"
    AGRICULTURE = "Сельхоз"
    RECREATION = "Рекреация"
    OTHER = "Прочее"


@dataclass
class Parcel:
    """Земельный участок"""
    cadastral_number: str
    address: str
    area: float  # Площадь в кв.м
    category: LandCategory
    price: float  # Цена аренды/НСПД в руб/год
    id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def validate(self) -> bool:
        """Базовая валидация участка"""
        if not self.cadastral_number or len(self.cadastral_number) < 5:
            return False
        if self.area <= 0:
            return False
        if self.price < 0:
            return False
        return True


class ApplicationStatus(str, Enum):
    """Статус заявки на получение аренды"""
    DRAFT = "Черновик"
    SUBMITTED = "Подана"
    IN_PROGRESS = "В обработке"
    APPROVED = "Одобрена"
    REJECTED = "Отклонена"


@dataclass
class Application:
    """Заявка на получение аренды через НСПД"""
    parcel_id: int
    status: ApplicationStatus
    id: Optional[int] = None
    submitted_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    def can_submit(self) -> bool:
        """Можно ли подать заявку"""
        return self.status == ApplicationStatus.DRAFT


class DealStatus(str, Enum):
    """Статус сделки по продаже прав аренды"""
    NEGOTIATION = "Переговоры"
    CONTRACT_SIGNING = "Подписание договора"
    PAYMENT_PENDING = "Ожидание оплаты"
    COMPLETED = "Завершена"
    CANCELLED = "Отменена"


@dataclass
class Deal:
    """Сделка по продаже прав аренды"""
    parcel_id: int
    sale_price: float  # Цена продажи прав аренды
    buyer_name: str
    buyer_contact: str
    status: DealStatus
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def mark_completed(self) -> None:
        """Отметить сделку как завершённую"""
        self.status = DealStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def calculate_profit(self, original_price: float) -> float:
        """Рассчитать прибыль от сделки"""
        return self.sale_price - original_price
