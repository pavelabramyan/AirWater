"""
Порты (интерфейсы) для репозиториев и внешних сервисов
"""
from typing import Protocol, List, Optional
from domain.models import Parcel, Application, Deal


class ParcelRepository(Protocol):
    """Интерфейс репозитория участков"""
    
    def add(self, parcel: Parcel) -> Parcel:
        """Добавить участок"""
        ...
    
    def get(self, parcel_id: int) -> Optional[Parcel]:
        """Получить участок по ID"""
        ...
    
    def list_all(self) -> List[Parcel]:
        """Получить все участки"""
        ...
    
    def update(self, parcel: Parcel) -> Parcel:
        """Обновить участок"""
        ...


class ApplicationRepository(Protocol):
    """Интерфейс репозитория заявок"""
    
    def add(self, application: Application) -> Application:
        """Добавить заявку"""
        ...
    
    def get(self, application_id: int) -> Optional[Application]:
        """Получить заявку по ID"""
        ...
    
    def list_all(self) -> List[Application]:
        """Получить все заявки"""
        ...
    
    def list_for_parcel(self, parcel_id: int) -> List[Application]:
        """Получить заявки для участка"""
        ...
    
    def update(self, application: Application) -> Application:
        """Обновить заявку"""
        ...


class DealRepository(Protocol):
    """Интерфейс репозитория сделок"""
    
    def add(self, deal: Deal) -> Deal:
        """Добавить сделку"""
        ...
    
    def get(self, deal_id: int) -> Optional[Deal]:
        """Получить сделку по ID"""
        ...
    
    def list_all(self) -> List[Deal]:
        """Получить все сделки"""
        ...
    
    def list_for_parcel(self, parcel_id: int) -> List[Deal]:
        """Получить сделки для участка"""
        ...
    
    def update(self, deal: Deal) -> Deal:
        """Обновить сделку"""
        ...
