"""
CLI интерфейс для управления системой "Фабрика участков"
"""
import logging
from datetime import datetime
from typing import Optional

from domain.models import LandCategory, ApplicationStatus, DealStatus
from application.storage_service import StorageService
from infrastructure.db import init_database
from infrastructure.sqlite_repositories import (
    SQLiteParcelRepository,
    SQLiteApplicationRepository,
    SQLiteDealRepository
)
import config

logger = logging.getLogger(__name__)


class CLI:
    """Командная строка для работы с системой"""
    
    def __init__(self, service: StorageService):
        self.service = service
    
    def run(self):
        """Запуск интерактивного режима"""
        print("=" * 60)
        print("Фабрика участков - Система управления земельными участками")
        print("=" * 60)
        
        while True:
            print("\nДоступные команды:")
            print("1. Добавить участок")
            print("2. Список участков")
            print("3. Добавить заявку")
            print("4. Список заявок")
            print("5. Добавить сделку")
            print("6. Список сделок")
            print("7. Аналитика")
            print("0. Выход")
            
            choice = input("\nВыберите команду: ").strip()
            
            try:
                if choice == "1":
                    self._add_parcel()
                elif choice == "2":
                    self._list_parcels()
                elif choice == "3":
                    self._add_application()
                elif choice == "4":
                    self._list_applications()
                elif choice == "5":
                    self._add_deal()
                elif choice == "6":
                    self._list_deals()
                elif choice == "7":
                    self._show_analytics()
                elif choice == "0":
                    print("До свидания!")
                    break
                else:
                    print("Неизвестная команда")
            except Exception as e:
                logger.error(f"Ошибка выполнения команды: {e}", exc_info=True)
                print(f"Ошибка: {e}")
    
    def _add_parcel(self):
        """Добавление участка"""
        print("\n--- Добавление участка ---")
        
        cadastral_number = input("Кадастровый номер: ").strip()
        address = input("Адрес: ").strip()
        area = float(input("Площадь (кв.м): ").strip())
        
        print("\nКатегория земли:")
        for i, cat in enumerate(LandCategory, 1):
            print(f"{i}. {cat.value}")
        cat_choice = int(input("Выберите категорию: ").strip()) - 1
        category = list(LandCategory)[cat_choice]
        
        price = float(input("Цена аренды/НСПД (руб/год): ").strip())
        
        parcel = self.service.add_parcel(
            cadastral_number=cadastral_number,
            address=address,
            area=area,
            category=category,
            price=price
        )
        
        print(f"\n✓ Участок добавлен с ID: {parcel.id}")
    
    def _list_parcels(self):
        """Список участков"""
        print("\n--- Список участков ---")
        parcels = self.service.get_all_parcels()
        
        if not parcels:
            print("Участков пока нет")
            return
        
        for p in parcels:
            print(f"\nID: {p.id}")
            print(f"  Кадастровый №: {p.cadastral_number}")
            print(f"  Адрес: {p.address}")
            print(f"  Площадь: {p.area} кв.м")
            print(f"  Категория: {p.category.value}")
            print(f"  Цена: {p.price:,.0f} руб/год")
            if p.metadata:
                print(f"  Метаданные: {p.metadata}")
    
    def _add_application(self):
        """Добавление заявки"""
        print("\n--- Добавление заявки ---")
        
        parcel_id = int(input("ID участка: ").strip())
        
        print("\nСтатус:")
        for i, status in enumerate(ApplicationStatus, 1):
            print(f"{i}. {status.value}")
        status_choice = int(input("Выберите статус: ").strip()) - 1
        status = list(ApplicationStatus)[status_choice]
        
        notes = input("Примечания (необязательно): ").strip() or None
        
        app = self.service.add_application(
            parcel_id=parcel_id,
            status=status,
            notes=notes
        )
        
        print(f"\n✓ Заявка добавлена с ID: {app.id}")
    
    def _list_applications(self):
        """Список заявок"""
        print("\n--- Список заявок ---")
        apps = self.service.get_all_applications()
        
        if not apps:
            print("Заявок пока нет")
            return
        
        for app in apps:
            parcel = self.service.get_parcel(app.parcel_id)
            print(f"\nID: {app.id}")
            print(f"  Участок: {parcel.cadastral_number if parcel else 'N/A'}")
            print(f"  Статус: {app.status.value}")
            print(f"  Дата подачи: {app.submitted_at.strftime('%Y-%m-%d %H:%M')}")
            if app.notes:
                print(f"  Примечания: {app.notes}")
    
    def _add_deal(self):
        """Добавление сделки"""
        print("\n--- Добавление сделки ---")
        
        parcel_id = int(input("ID участка: ").strip())
        sale_price = float(input("Цена продажи (руб): ").strip())
        buyer_name = input("Имя покупателя: ").strip()
        buyer_contact = input("Контакт покупателя: ").strip()
        
        print("\nСтатус сделки:")
        for i, status in enumerate(DealStatus, 1):
            print(f"{i}. {status.value}")
        status_choice = int(input("Выберите статус: ").strip()) - 1
        status = list(DealStatus)[status_choice]
        
        deal = self.service.add_deal(
            parcel_id=parcel_id,
            sale_price=sale_price,
            buyer_name=buyer_name,
            buyer_contact=buyer_contact,
            status=status
        )
        
        print(f"\n✓ Сделка добавлена с ID: {deal.id}")
    
    def _list_deals(self):
        """Список сделок"""
        print("\n--- Список сделок ---")
        deals = self.service.get_all_deals()
        
        if not deals:
            print("Сделок пока нет")
            return
        
        for deal in deals:
            parcel = self.service.get_parcel(deal.parcel_id)
            print(f"\nID: {deal.id}")
            print(f"  Участок: {parcel.cadastral_number if parcel else 'N/A'}")
            print(f"  Покупатель: {deal.buyer_name}")
            print(f"  Контакт: {deal.buyer_contact}")
            print(f"  Цена продажи: {deal.sale_price:,.0f} руб")
            print(f"  Статус: {deal.status.value}")
            print(f"  Дата создания: {deal.created_at.strftime('%Y-%m-%d %H:%M')}")
            if deal.completed_at:
                print(f"  Дата завершения: {deal.completed_at.strftime('%Y-%m-%d %H:%M')}")
    
    def _show_analytics(self):
        """Показать аналитику"""
        print("\n" + "=" * 60)
        print("АНАЛИТИКА СИСТЕМЫ")
        print("=" * 60)
        
        analytics = self.service.get_analytics()
        
        print(f"\n📊 Участки:")
        print(f"  Всего участков: {analytics['total_parcels']}")
        print(f"  Общая площадь: {analytics['total_area']:,.0f} кв.м")
        print(f"  Средняя площадь: {analytics['avg_area']:,.0f} кв.м")
        
        print(f"\n📝 Заявки:")
        print(f"  Всего заявок: {analytics['total_applications']}")
        for status, count in analytics['applications_by_status'].items():
            print(f"    {status}: {count}")
        
        print(f"\n💰 Сделки:")
        print(f"  Всего сделок: {analytics['total_deals']}")
        print(f"  Завершённых: {analytics['completed_deals']}")
        for status, count in analytics['deals_by_status'].items():
            print(f"    {status}: {count}")
        
        if analytics['total_revenue'] > 0:
            print(f"\n💵 Финансы:")
            print(f"  Общая выручка: {analytics['total_revenue']:,.0f} руб")
            print(f"  Средний чек: {analytics['avg_deal_price']:,.0f} руб")
            
            if analytics['potential_profit'] > 0:
                print(f"  Потенциальная прибыль: {analytics['potential_profit']:,.0f} руб")


def main():
    """Точка входа CLI"""
    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    logger.info("Запуск CLI")
    
    # Инициализация БД
    init_database(config.DATABASE_PATH)
    
    # Создание репозиториев
    parcel_repo = SQLiteParcelRepository(config.DATABASE_PATH)
    app_repo = SQLiteApplicationRepository(config.DATABASE_PATH)
    deal_repo = SQLiteDealRepository(config.DATABASE_PATH)
    
    # Создание сервиса
    service = StorageService(parcel_repo, app_repo, deal_repo)
    
    # Запуск CLI
    cli = CLI(service)
    cli.run()


if __name__ == "__main__":
    main()















