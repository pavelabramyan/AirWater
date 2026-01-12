"""
Порты (интерфейсы) для модуля поиска
"""
from typing import Protocol, List
from .domain import SearchCriteria, FoundParcel


class ParcelDataSource(Protocol):
    """Интерфейс источника данных об участках"""
    
    def search(self, criteria: SearchCriteria) -> List[FoundParcel]:
        """Поиск участков по критериям"""
        ...
    
    def get_parcel_details(self, cadastral_number: str) -> FoundParcel:
        """Получить детальную информацию об участке"""
        ...
    
    def is_available(self) -> bool:
        """Проверка доступности источника"""
        ...















