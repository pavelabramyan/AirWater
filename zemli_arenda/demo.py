#!/usr/bin/env python3
"""
Демо-скрипт для проверки работы системы "Фабрика участков"
"""
import logging
from domain.models import LandCategory, ApplicationStatus, DealStatus
from application.storage_service import StorageService
from infrastructure.db import init_database
from infrastructure.sqlite_repositories import (
    SQLiteParcelRepository,
    SQLiteApplicationRepository,
    SQLiteDealRepository
)
import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Демонстрация возможностей системы"""
    logger.info("=== ДЕМО: Фабрика участков ===")
    
    # Инициализация БД
    logger.info("Инициализация базы данных...")
    init_database(config.DATABASE_PATH)
    
    # Создание репозиториев
    parcel_repo = SQLiteParcelRepository(config.DATABASE_PATH)
    app_repo = SQLiteApplicationRepository(config.DATABASE_PATH)
    deal_repo = SQLiteDealRepository(config.DATABASE_PATH)
    
    # Создание сервиса
    service = StorageService(parcel_repo, app_repo, deal_repo)
    
    # 1. Добавление участков
    logger.info("\n1. Добавление участков...")
    
    parcel1 = service.add_parcel(
        cadastral_number="74:36:0123456:001",
        address="г. Челябинск, Ленинский район, ул. Южная, уч. 10",
        area=1200.0,
        category=LandCategory.IZhS,
        price=60000.0,
        metadata={"distance_km": 15, "infrastructure": "частичная"}
    )
    logger.info(f"  ✓ Участок {parcel1.cadastral_number} добавлен (ID: {parcel1.id})")
    
    parcel2 = service.add_parcel(
        cadastral_number="74:36:0123456:002",
        address="г. Челябинск, Советский район, ул. Лесная, уч. 25",
        area=800.0,
        category=LandCategory.LPKh,
        price=40000.0,
        metadata={"distance_km": 20, "infrastructure": "отсутствует"}
    )
    logger.info(f"  ✓ Участок {parcel2.cadastral_number} добавлен (ID: {parcel2.id})")
    
    parcel3 = service.add_parcel(
        cadastral_number="74:36:0123456:003",
        address="г. Челябинск, Калининский район, ул. Речная, уч. 5",
        area=1500.0,
        category=LandCategory.COMMERCE,
        price=150000.0,
        metadata={"distance_km": 10, "infrastructure": "полная"}
    )
    logger.info(f"  ✓ Участок {parcel3.cadastral_number} добавлен (ID: {parcel3.id})")
    
    # 2. Добавление заявок
    logger.info("\n2. Создание заявок на получение аренды...")
    
    app1 = service.add_application(
        parcel_id=parcel1.id,
        status=ApplicationStatus.SUBMITTED,
        notes="Заявка подана через МФЦ"
    )
    logger.info(f"  ✓ Заявка #{app1.id} для участка {parcel1.cadastral_number}")
    
    app2 = service.add_application(
        parcel_id=parcel2.id,
        status=ApplicationStatus.IN_PROGRESS,
        notes="Документы на проверке в администрации"
    )
    logger.info(f"  ✓ Заявка #{app2.id} для участка {parcel2.cadastral_number}")
    
    app3 = service.add_application(
        parcel_id=parcel3.id,
        status=ApplicationStatus.APPROVED,
        notes="Аренда одобрена, ожидаем договор"
    )
    logger.info(f"  ✓ Заявка #{app3.id} для участка {parcel3.cadastral_number}")
    
    # 3. Добавление сделок
    logger.info("\n3. Регистрация сделок по продаже прав аренды...")
    
    deal1 = service.add_deal(
        parcel_id=parcel3.id,
        sale_price=600000.0,
        buyer_name="Иванов Иван Иванович",
        buyer_contact="+7 900 123-45-67",
        status=DealStatus.NEGOTIATION
    )
    logger.info(f"  ✓ Сделка #{deal1.id} на {deal1.sale_price:,.0f} руб (переговоры)")
    
    deal2 = service.add_deal(
        parcel_id=parcel1.id,
        sale_price=450000.0,
        buyer_name="Петров Петр Петрович",
        buyer_contact="+7 901 234-56-78",
        status=DealStatus.COMPLETED
    )
    logger.info(f"  ✓ Сделка #{deal2.id} на {deal2.sale_price:,.0f} руб (завершена)")
    
    # 4. Получение аналитики
    logger.info("\n4. Аналитика системы:")
    logger.info("=" * 60)
    
    analytics = service.get_analytics()
    
    logger.info(f"\n📊 Участки:")
    logger.info(f"  Всего участков: {analytics['total_parcels']}")
    logger.info(f"  Общая площадь: {analytics['total_area']:,.0f} кв.м")
    logger.info(f"  Средняя площадь: {analytics['avg_area']:,.0f} кв.м")
    
    logger.info(f"\n📝 Заявки:")
    logger.info(f"  Всего заявок: {analytics['total_applications']}")
    for status, count in analytics['applications_by_status'].items():
        logger.info(f"    {status}: {count}")
    
    logger.info(f"\n💰 Сделки:")
    logger.info(f"  Всего сделок: {analytics['total_deals']}")
    logger.info(f"  Завершённых: {analytics['completed_deals']}")
    for status, count in analytics['deals_by_status'].items():
        logger.info(f"    {status}: {count}")
    
    logger.info(f"\n💵 Финансы:")
    logger.info(f"  Общая выручка: {analytics['total_revenue']:,.0f} руб")
    logger.info(f"  Средний чек: {analytics['avg_deal_price']:,.0f} руб")
    logger.info(f"  Потенциальная прибыль: {analytics['potential_profit']:,.0f} руб")
    
    logger.info("\n" + "=" * 60)
    logger.info("✓ ДЕМО завершено успешно!")
    logger.info("\nДля работы с системой используйте:")
    logger.info("  - CLI: python run_cli.py")
    logger.info("  - Web: python run_web.py")


if __name__ == "__main__":
    main()















