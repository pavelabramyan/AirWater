"""
Сервис учёта и аналитики участков, заявок и сделок
"""
import logging
from typing import Dict, Any, List
from domain.models import Parcel, Application, Deal, LandCategory, ApplicationStatus, DealStatus
from .ports import ParcelRepository, ApplicationRepository, DealRepository

logger = logging.getLogger(__name__)


class StorageService:
    """Сервис для работы с участками, заявками и сделками"""
    
    def __init__(
        self,
        parcel_repo: ParcelRepository,
        application_repo: ApplicationRepository,
        deal_repo: DealRepository
    ):
        self.parcel_repo = parcel_repo
        self.application_repo = application_repo
        self.deal_repo = deal_repo
    
    # Участки
    def add_parcel(
        self,
        cadastral_number: str,
        address: str,
        area: float,
        category: LandCategory,
        price: float,
        metadata: Dict[str, Any] = None
    ) -> Parcel:
        """Добавить новый участок"""
        logger.info(f"Добавление участка {cadastral_number}")
        
        parcel = Parcel(
            cadastral_number=cadastral_number,
            address=address,
            area=area,
            category=category,
            price=price,
            metadata=metadata
        )
        
        if not parcel.validate():
            raise ValueError("Некорректные данные участка")
        
        created = self.parcel_repo.add(parcel)
        logger.info(f"Участок добавлен с ID: {created.id}")
        return created
    
    def get_parcel(self, parcel_id: int) -> Parcel:
        """Получить участок по ID"""
        return self.parcel_repo.get(parcel_id)
    
    def get_all_parcels(self) -> List[Parcel]:
        """Получить все участки"""
        return self.parcel_repo.list_all()
    
    # Заявки
    def add_application(
        self,
        parcel_id: int,
        status: ApplicationStatus,
        notes: str = None
    ) -> Application:
        """Добавить новую заявку"""
        logger.info(f"Добавление заявки для участка ID: {parcel_id}")
        
        application = Application(
            parcel_id=parcel_id,
            status=status,
            notes=notes
        )
        
        created = self.application_repo.add(application)
        logger.info(f"Заявка добавлена с ID: {created.id}")
        return created
    
    def get_application(self, application_id: int) -> Application:
        """Получить заявку по ID"""
        return self.application_repo.get(application_id)
    
    def get_all_applications(self) -> List[Application]:
        """Получить все заявки"""
        return self.application_repo.list_all()
    
    def get_applications_for_parcel(self, parcel_id: int) -> List[Application]:
        """Получить заявки для участка"""
        return self.application_repo.list_for_parcel(parcel_id)
    
    # Сделки
    def add_deal(
        self,
        parcel_id: int,
        sale_price: float,
        buyer_name: str,
        buyer_contact: str,
        status: DealStatus
    ) -> Deal:
        """Добавить новую сделку"""
        logger.info(f"Добавление сделки для участка ID: {parcel_id}")
        
        deal = Deal(
            parcel_id=parcel_id,
            sale_price=sale_price,
            buyer_name=buyer_name,
            buyer_contact=buyer_contact,
            status=status
        )
        
        created = self.deal_repo.add(deal)
        logger.info(f"Сделка добавлена с ID: {created.id}")
        return created
    
    def get_deal(self, deal_id: int) -> Deal:
        """Получить сделку по ID"""
        return self.deal_repo.get(deal_id)
    
    def get_all_deals(self) -> List[Deal]:
        """Получить все сделки"""
        return self.deal_repo.list_all()
    
    def get_deals_for_parcel(self, parcel_id: int) -> List[Deal]:
        """Получить сделки для участка"""
        return self.deal_repo.list_for_parcel(parcel_id)
    
    # Аналитика
    def get_analytics(self) -> Dict[str, Any]:
        """Получить аналитику по системе"""
        logger.info("Расчёт аналитики")
        
        parcels = self.get_all_parcels()
        applications = self.get_all_applications()
        deals = self.get_all_deals()
        
        # Участки
        total_parcels = len(parcels)
        total_area = sum(p.area for p in parcels)
        avg_area = total_area / total_parcels if total_parcels > 0 else 0
        
        # Заявки
        total_applications = len(applications)
        applications_by_status = {}
        for app in applications:
            status = app.status.value
            applications_by_status[status] = applications_by_status.get(status, 0) + 1
        
        # Сделки
        total_deals = len(deals)
        completed_deals = len([d for d in deals if d.status == DealStatus.COMPLETED])
        deals_by_status = {}
        for deal in deals:
            status = deal.status.value
            deals_by_status[status] = deals_by_status.get(status, 0) + 1
        
        # Финансы
        total_revenue = sum(d.sale_price for d in deals if d.status == DealStatus.COMPLETED)
        avg_deal_price = total_revenue / completed_deals if completed_deals > 0 else 0
        
        # Потенциальная прибыль от активных сделок
        potential_profit = sum(
            d.sale_price for d in deals 
            if d.status in [DealStatus.NEGOTIATION, DealStatus.CONTRACT_SIGNING, DealStatus.PAYMENT_PENDING]
        )
        
        return {
            "total_parcels": total_parcels,
            "total_area": total_area,
            "avg_area": avg_area,
            "total_applications": total_applications,
            "applications_by_status": applications_by_status,
            "total_deals": total_deals,
            "completed_deals": completed_deals,
            "deals_by_status": deals_by_status,
            "total_revenue": total_revenue,
            "avg_deal_price": avg_deal_price,
            "potential_profit": potential_profit
        }
