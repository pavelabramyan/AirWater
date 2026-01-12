"""
Веб-интерфейс для управления системой "Фабрика участков"
Минималистичный UI на Flask с Pico CSS
"""
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from domain.models import LandCategory, ApplicationStatus, DealStatus
from application.storage_service import StorageService
from infrastructure.db import init_database
from infrastructure.sqlite_repositories import (
    SQLiteParcelRepository,
    SQLiteApplicationRepository,
    SQLiteDealRepository
)
from features.search.domain import SearchCriteria
from features.search.pkk_parser import PKKDataSource
from features.search.service import SearchService
from features.search.regions import get_all_regions, get_popular_regions, get_region_bbox
import config

logger = logging.getLogger(__name__)

# Создание приложения
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = config.SECRET_KEY

# Инициализация БД и сервиса
init_database(config.DATABASE_PATH)
parcel_repo = SQLiteParcelRepository(config.DATABASE_PATH)
app_repo = SQLiteApplicationRepository(config.DATABASE_PATH)
deal_repo = SQLiteDealRepository(config.DATABASE_PATH)
service = StorageService(parcel_repo, app_repo, deal_repo)

# Инициализация сервиса поиска
pkk_source = PKKDataSource()
search_service = SearchService([pkk_source], parcel_repo)


@app.route('/')
def index():
    """Главная страница с дашбордом"""
    analytics = service.get_analytics()
    return render_template('index.html', analytics=analytics)


@app.route('/parcels')
def parcels_list():
    """Список участков"""
    parcels = service.get_all_parcels()
    return render_template('parcels.html', parcels=parcels)


@app.route('/parcels/add', methods=['GET', 'POST'])
def parcel_add():
    """Добавление участка"""
    if request.method == 'POST':
        try:
            parcel = service.add_parcel(
                cadastral_number=request.form['cadastral_number'],
                address=request.form['address'],
                area=float(request.form['area']),
                category=LandCategory(request.form['category']),
                price=float(request.form['price'])
            )
            flash(f'Участок {parcel.cadastral_number} успешно добавлен', 'success')
            return redirect(url_for('parcels_list'))
        except Exception as e:
            logger.error(f"Ошибка добавления участка: {e}", exc_info=True)
            flash(f'Ошибка: {e}', 'error')
    
    categories = [cat.value for cat in LandCategory]
    return render_template('parcel_form.html', categories=categories)


@app.route('/applications')
def applications_list():
    """Список заявок"""
    apps = service.get_all_applications()
    # Обогащаем данными участков
    apps_with_parcels = []
    for app in apps:
        parcel = service.get_parcel(app.parcel_id)
        apps_with_parcels.append({
            'application': app,
            'parcel': parcel
        })
    return render_template('applications.html', applications=apps_with_parcels)


@app.route('/applications/add', methods=['GET', 'POST'])
def application_add():
    """Добавление заявки"""
    if request.method == 'POST':
        try:
            app = service.add_application(
                parcel_id=int(request.form['parcel_id']),
                status=ApplicationStatus(request.form['status']),
                notes=request.form.get('notes') or None
            )
            flash(f'Заявка #{app.id} успешно добавлена', 'success')
            return redirect(url_for('applications_list'))
        except Exception as e:
            logger.error(f"Ошибка добавления заявки: {e}", exc_info=True)
            flash(f'Ошибка: {e}', 'error')
    
    parcels = service.get_all_parcels()
    statuses = [status.value for status in ApplicationStatus]
    return render_template('application_form.html', parcels=parcels, statuses=statuses)


@app.route('/deals')
def deals_list():
    """Список сделок"""
    deals = service.get_all_deals()
    # Обогащаем данными участков
    deals_with_parcels = []
    for deal in deals:
        parcel = service.get_parcel(deal.parcel_id)
        deals_with_parcels.append({
            'deal': deal,
            'parcel': parcel
        })
    return render_template('deals.html', deals=deals_with_parcels)


@app.route('/deals/add', methods=['GET', 'POST'])
def deal_add():
    """Добавление сделки"""
    if request.method == 'POST':
        try:
            deal = service.add_deal(
                parcel_id=int(request.form['parcel_id']),
                sale_price=float(request.form['sale_price']),
                buyer_name=request.form['buyer_name'],
                buyer_contact=request.form['buyer_contact'],
                status=DealStatus(request.form['status'])
            )
            flash(f'Сделка #{deal.id} успешно добавлена', 'success')
            return redirect(url_for('deals_list'))
        except Exception as e:
            logger.error(f"Ошибка добавления сделки: {e}", exc_info=True)
            flash(f'Ошибка: {e}', 'error')
    
    parcels = service.get_all_parcels()
    statuses = [status.value for status in DealStatus]
    return render_template('deal_form.html', parcels=parcels, statuses=statuses)


@app.route('/analytics')
def analytics():
    """Страница аналитики"""
    analytics = service.get_analytics()
    return render_template('analytics.html', analytics=analytics)


@app.route('/api/analytics')
def api_analytics():
    """API для получения аналитики"""
    return jsonify(service.get_analytics())


@app.route('/search')
def search_page():
    """Страница поиска участков"""
    all_regions = get_all_regions()
    popular_regions = get_popular_regions()
    return render_template('search.html', all_regions=all_regions, popular_regions=popular_regions)


@app.route('/search/run', methods=['POST'])
def run_search():
    """Запуск поиска участков"""
    try:
        # Получение параметров поиска
        region_code = request.form.get('region_code', '74')
        min_area = float(request.form.get('min_area', 0)) if request.form.get('min_area') else None
        max_area = float(request.form.get('max_area', 0)) if request.form.get('max_area') else None
        
        # Создание критериев поиска
        criteria = SearchCriteria(
            region_code=region_code,
            min_area=min_area,
            max_area=max_area,
            only_free=request.form.get('only_free', 'true') == 'true'
        )
        
        # Bbox если указан
        bbox_str = request.form.get('bbox')
        if bbox_str:
            try:
                parts = bbox_str.split(',')
                criteria.bbox = {
                    'min_lon': float(parts[0]),
                    'min_lat': float(parts[1]),
                    'max_lon': float(parts[2]),
                    'max_lat': float(parts[3])
                }
            except:
                flash('Некорректный формат bbox', 'error')
                return redirect(url_for('search_page'))
        
        # Запуск поиска
        logger.info(f"Запуск поиска с критериями: {criteria}")
        result = search_service.search_parcels(criteria)
        
        # Сохранение результата в сессии для последующего просмотра
        # (в продакшене лучше использовать кэш или БД)
        top_parcels = result.get_top_parcels(20)
        
        flash(f'Поиск завершён! Найдено: {result.total_found}, подходящих: {result.filtered_count}', 'success')
        return render_template('search_results.html', result=result, top_parcels=top_parcels)
    
    except Exception as e:
        logger.error(f"Ошибка поиска: {e}", exc_info=True)
        flash(f'Ошибка поиска: {e}', 'error')
        return redirect(url_for('search_page'))


@app.route('/search/import/<cadastral_number>', methods=['POST'])
def import_found_parcel(cadastral_number):
    """Импорт найденного участка в систему"""
    try:
        # Получение деталей участка
        found_parcel = search_service.get_parcel_details(cadastral_number)
        if not found_parcel:
            flash(f'Участок {cadastral_number} не найден', 'error')
            return redirect(url_for('search_page'))
        
        # Импорт
        rent = float(request.form.get('rent', 50000))
        parcel = search_service.import_parcel(found_parcel, rent)
        
        flash(f'Участок {parcel.cadastral_number} успешно импортирован (ID: {parcel.id})', 'success')
        return redirect(url_for('parcels_list'))
    
    except Exception as e:
        logger.error(f"Ошибка импорта: {e}", exc_info=True)
        flash(f'Ошибка импорта: {e}', 'error')
        return redirect(url_for('search_page'))


def main():
    """Запуск веб-сервера"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    logger.info(f"Запуск веб-сервера на {config.WEB_HOST}:{config.WEB_PORT}")
    app.run(host=config.WEB_HOST, port=config.WEB_PORT, debug=True)


if __name__ == '__main__':
    main()

