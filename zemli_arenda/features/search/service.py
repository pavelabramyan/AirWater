"""
Сервис поиска земельных участков
"""
import logging
from datetime import datetime
from typing import List, Optional

from .domain import SearchCriteria, SearchResult, FoundParcel, ParcelSource
from .ports import ParcelDataSource
from domain.models import Parcel, LandCategory
from application.ports import ParcelRepository

logger = logging.getLogger(__name__)


class SearchService:
    """Сервис для поиска и импорта участков"""
    
    def __init__(
        self,
        data_sources: List[ParcelDataSource],
        parcel_repo: ParcelRepository
    ):
        self.data_sources = data_sources
        self.parcel_repo = parcel_repo
    
    def search_parcels(self, criteria: SearchCriteria) -> SearchResult:
        """Поиск участков по критериям"""
        logger.info(f"Запуск поиска участков в регионе {criteria.region_code}")
        
        search_started_at = datetime.now()
        all_found_parcels = []
        errors = []
        
        # Поиск во всех доступных источниках
        for source in self.data_sources:
            try:
                if not source.is_available():
                    logger.warning(f"Источник {source.__class__.__name__} недоступен")
                    errors.append(f"{source.__class__.__name__}: недоступен")
                    continue
                
                logger.info(f"Поиск через {source.__class__.__name__}")
                parcels = source.search(criteria)
                all_found_parcels.extend(parcels)
                logger.info(f"Найдено {len(parcels)} участков через {source.__class__.__name__}")
            
            except Exception as e:
                logger.error(f"Ошибка поиска через {source.__class__.__name__}: {e}", exc_info=True)
                errors.append(f"{source.__class__.__name__}: {str(e)}")
        
        search_completed_at = datetime.now()
        
        # Удаление дубликатов по кадастровому номеру
        unique_parcels = self._remove_duplicates(all_found_parcels)
        
        # Фильтрация подходящих
        suitable_parcels = [p for p in unique_parcels if p.is_suitable()]
        
        result = SearchResult(
            criteria=criteria,
            found_parcels=unique_parcels,
            total_found=len(unique_parcels),
            filtered_count=len(suitable_parcels),
            search_started_at=search_started_at,
            search_completed_at=search_completed_at,
            errors=errors
        )
        
        logger.info(f"Поиск завершён: найдено {result.total_found}, подходящих {result.filtered_count}")
        return result
    
    def _remove_duplicates(self, parcels: List[FoundParcel]) -> List[FoundParcel]:
        """Удаление дубликатов участков"""
        seen = set()
        unique = []
        
        for parcel in parcels:
            if parcel.cadastral_number not in seen:
                seen.add(parcel.cadastral_number)
                unique.append(parcel)
        
        return unique
    
    def import_parcel(self, found_parcel: FoundParcel, estimated_rent: float) -> Parcel:
        """Импорт найденного участка в основную систему"""
        logger.info(f"Импорт участка {found_parcel.cadastral_number}")
        
        # Маппинг категории
        category = self._map_category(found_parcel.category)
        
        # Создание участка
        parcel = Parcel(
            cadastral_number=found_parcel.cadastral_number,
            address=found_parcel.address,
            area=found_parcel.area,
            category=category,
            price=estimated_rent,
            metadata={
                'source': found_parcel.source.value,
                'availability': found_parcel.availability.value,
                'district': found_parcel.district,
                'coordinates': found_parcel.coordinates,
                'priority_score': found_parcel.calculate_priority_score(),
                'imported_at': datetime.now().isoformat(),
                'raw_data': found_parcel.raw_data
            }
        )
        
        # Валидация и сохранение
        if not parcel.validate():
            raise ValueError(f"Некорректные данные участка {found_parcel.cadastral_number}")
        
        created = self.parcel_repo.add(parcel)
        logger.info(f"Участок импортирован с ID: {created.id}")
        
        return created
    
    def _map_category(self, pkk_category: str) -> LandCategory:
        """Маппинг категории из PKK в систему"""
        category_map = {
            'ИЖС': LandCategory.IZhS,
            'ЛПХ': LandCategory.LPKh,
            'Садоводство': LandCategory.AGRICULTURE,
            'Огородничество': LandCategory.AGRICULTURE,
            'Коммерческая': LandCategory.COMMERCE,
            'Рекреация': LandCategory.RECREATION,
        }
        
        return category_map.get(pkk_category, LandCategory.OTHER)
    
    def import_multiple(
        self,
        found_parcels: List[FoundParcel],
        default_rent: float = 50000.0
    ) -> List[Parcel]:
        """Массовый импорт найденных участков"""
        logger.info(f"Массовый импорт {len(found_parcels)} участков")
        
        imported = []
        for found_parcel in found_parcels:
            try:
                # Расчёт примерной арендной ставки (можно улучшить)
                estimated_rent = self._estimate_rent(found_parcel, default_rent)
                parcel = self.import_parcel(found_parcel, estimated_rent)
                imported.append(parcel)
            except Exception as e:
                logger.error(f"Ошибка импорта {found_parcel.cadastral_number}: {e}")
                continue
        
        logger.info(f"Успешно импортировано: {len(imported)}/{len(found_parcels)}")
        return imported
    
    def _estimate_rent(self, found_parcel: FoundParcel, base_rate: float) -> float:
        """Оценка арендной ставки"""
        # Базовая ставка
        rent = base_rate
        
        # Коррекция по площади (чем больше, тем дороже)
        if found_parcel.area > 1500:
            rent *= 1.5
        elif found_parcel.area < 800:
            rent *= 0.7
        
        # Коррекция по категории
        if found_parcel.category == "ИЖС":
            rent *= 1.3
        elif found_parcel.category == "Коммерческая":
            rent *= 2.0
        
        # Коррекция по наличию адреса
        if found_parcel.address and len(found_parcel.address) > 20:
            rent *= 1.1
        
        return round(rent, -3)  # Округление до тысяч
    
    def get_parcel_details(self, cadastral_number: str) -> Optional[FoundParcel]:
        """Получить детальную информацию об участке"""
        logger.info(f"Получение деталей участка {cadastral_number}")
        
        for source in self.data_sources:
            try:
                if source.is_available():
                    details = source.get_parcel_details(cadastral_number)
                    if details:
                        return details
            except Exception as e:
                logger.warning(f"Ошибка получения деталей из {source.__class__.__name__}: {e}")
        
        return None















