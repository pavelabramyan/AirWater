"""
Парсер Публичной кадастровой карты Росреестра
Использует публичное API PKK5
"""
import logging
from typing import List, Optional
import aiohttp
import asyncio
from datetime import datetime

from .domain import FoundParcel, SearchCriteria, ParcelSource, ParcelAvailability
from .ports import ParcelDataSource

logger = logging.getLogger(__name__)


class PKKParser:
    """Парсер публичной кадастровой карты"""
    
    # Базовые URL API PKK
    BASE_URL = "https://pkk.rosreestr.ru/api"
    FEATURES_URL = f"{BASE_URL}/features"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    async def search(self, criteria: SearchCriteria) -> List[FoundParcel]:
        """Поиск участков по критериям"""
        logger.info(f"Начало поиска участков в регионе {criteria.region_code}")
        
        if not criteria.validate():
            logger.error("Некорректные критерии поиска")
            return []
        
        found_parcels = []
        
        try:
            # Если указаны границы поиска
            if criteria.bbox:
                parcels = await self._search_by_bbox(criteria)
                found_parcels.extend(parcels)
            else:
                logger.warning("Поиск без bbox пока не реализован")
        
        except Exception as e:
            logger.error(f"Ошибка при поиске участков: {e}", exc_info=True)
        
        logger.info(f"Найдено участков: {len(found_parcels)}")
        return found_parcels
    
    async def _search_by_bbox(self, criteria: SearchCriteria) -> List[FoundParcel]:
        """Поиск участков по географическим границам"""
        bbox = criteria.bbox
        if not bbox:
            return []
        
        # Формируем запрос к API PKK
        # Пример: https://pkk.rosreestr.ru/api/features/1?text=&tolerance=4&limit=40
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.FEATURES_URL}/1"  # 1 = земельные участки
            params = {
                'bbox': f"{bbox['min_lon']},{bbox['min_lat']},{bbox['max_lon']},{bbox['max_lat']}",
                'limit': 100,
                'tolerance': 4
            }
            
            try:
                async with session.get(url, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        logger.error(f"PKK API вернул статус {response.status}")
                        return []
                    
                    data = await response.json()
                    return self._parse_features(data, criteria)
            
            except asyncio.TimeoutError:
                logger.error("Timeout при запросе к PKK API")
                return []
            except Exception as e:
                logger.error(f"Ошибка запроса к PKK: {e}", exc_info=True)
                return []
    
    def _parse_features(self, data: dict, criteria: SearchCriteria) -> List[FoundParcel]:
        """Парсинг ответа от PKK API"""
        parcels = []
        
        features = data.get('features', [])
        logger.info(f"Обработка {len(features)} объектов из PKK")
        
        for feature in features:
            try:
                parcel = self._parse_single_feature(feature)
                if parcel and self._matches_criteria(parcel, criteria):
                    parcels.append(parcel)
            except Exception as e:
                logger.warning(f"Ошибка парсинга объекта: {e}")
                continue
        
        return parcels
    
    def _parse_single_feature(self, feature: dict) -> Optional[FoundParcel]:
        """Парсинг одного объекта"""
        attrs = feature.get('attrs', {})
        
        cadastral_number = attrs.get('cn')
        if not cadastral_number:
            return None
        
        # Координаты центра
        center = feature.get('center', {})
        coordinates = None
        if center:
            coordinates = {
                'lat': center.get('y'),
                'lon': center.get('x')
            }
        
        # Определение доступности
        availability = self._determine_availability(attrs)
        
        return FoundParcel(
            cadastral_number=cadastral_number,
            address=attrs.get('address', 'Адрес не указан'),
            area=float(attrs.get('area_value', 0)),
            category=attrs.get('category_type', 'Не указана'),
            source=ParcelSource.ROSREESTR_PKK,
            availability=availability,
            district=attrs.get('district_type'),
            coordinates=coordinates,
            has_owner=bool(attrs.get('rights')),
            has_encumbrances=bool(attrs.get('encumbrances')),
            purpose=attrs.get('util_by_doc'),
            raw_data=attrs
        )
    
    def _determine_availability(self, attrs: dict) -> ParcelAvailability:
        """Определение доступности участка"""
        # Проверка наличия правообладателя
        if attrs.get('rights'):
            return ParcelAvailability.HAS_OWNER
        
        # Проверка обременений
        if attrs.get('encumbrances'):
            return ParcelAvailability.ENCUMBERED
        
        # Проверка статуса государственной собственности
        ownership_type = attrs.get('fp', {}).get('ownership_type', '')
        if 'не разграничена' in ownership_type.lower():
            return ParcelAvailability.STATE_OWNERSHIP
        
        # По умолчанию считаем свободным
        return ParcelAvailability.FREE
    
    def _matches_criteria(self, parcel: FoundParcel, criteria: SearchCriteria) -> bool:
        """Проверка соответствия участка критериям"""
        # Площадь
        if criteria.min_area and parcel.area < criteria.min_area:
            return False
        if criteria.max_area and parcel.area > criteria.max_area:
            return False
        
        # Категории
        if criteria.categories and parcel.category not in criteria.categories:
            return False
        
        # Только свободные
        if criteria.only_free and not parcel.is_suitable():
            return False
        
        return True
    
    async def get_parcel_details(self, cadastral_number: str) -> Optional[FoundParcel]:
        """Получить детальную информацию об участке"""
        logger.info(f"Получение деталей участка {cadastral_number}")
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.FEATURES_URL}/1/{cadastral_number}"
            
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status != 200:
                        logger.error(f"PKK API вернул статус {response.status}")
                        return None
                    
                    data = await response.json()
                    feature = data.get('feature', {})
                    return self._parse_single_feature(feature)
            
            except Exception as e:
                logger.error(f"Ошибка получения деталей: {e}", exc_info=True)
                return None
    
    def is_available(self) -> bool:
        """Проверка доступности PKK API"""
        # Простая синхронная проверка
        try:
            import requests
            response = requests.get(self.BASE_URL, timeout=5)
            return response.status_code == 200
        except:
            return False


# Синхронная обёртка для удобства
class PKKDataSource:
    """Синхронная обёртка над PKKParser"""
    
    def __init__(self):
        self.parser = PKKParser()
    
    def search(self, criteria: SearchCriteria) -> List[FoundParcel]:
        """Синхронный поиск"""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.parser.search(criteria))
    
    def get_parcel_details(self, cadastral_number: str) -> Optional[FoundParcel]:
        """Синхронное получение деталей"""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.parser.get_parcel_details(cadastral_number))
    
    def is_available(self) -> bool:
        """Проверка доступности"""
        return self.parser.is_available()















