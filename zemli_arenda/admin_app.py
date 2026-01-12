#!/usr/bin/env python3
"""
Веб-админка для управления базой данных земельных участков
Запуск: python3 admin_app.py
Откроется: http://localhost:5000
"""

import os
import subprocess
import threading
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime
import math
import re

app = Flask(__name__)
DB_PATH = 'land_records.db'
ITEMS_PER_PAGE = 50
BOT_CONFIG_FILE = 'bot_config.json'
SMS_CODE_FILE = 'sms_code.txt'
BOT_PROCESS = None

def get_db_connection():
    """Подключение к БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def build_filter_query(filters):
    """Построить WHERE clause из фильтров"""
    conditions = []
    params = []
    
    for column, value in filters.items():
        if value and str(value).strip():
            # Специальная обработка для application_number
            if column == 'application_number':
                if value == 'NOT_EMPTY':
                    conditions.append(f"{column} IS NOT NULL AND {column} != ''")
                elif value == 'EMPTY':
                    conditions.append(f"({column} IS NULL OR {column} = '')")
                else:
                    # Поиск по конкретному номеру
                    conditions.append(f"{column} LIKE ?")
                    params.append(f"%{value.strip()}%")
            # Специальная обработка для ID (точное совпадение)
            elif column == 'id':
                conditions.append(f"{column} = ?")
                params.append(int(value))
            # Специальная обработка для диапазона дат
            elif column == 'date_from':
                conditions.append("DATE(submission_datetime) >= ?")
                params.append(value.strip())
            elif column == 'date_to':
                conditions.append("DATE(submission_datetime) <= ?")
                params.append(value.strip())
            # Специальная обработка для диапазона площади
            elif column == 'area_min':
                conditions.append("CAST(area AS REAL) >= ?")
                params.append(float(value))
            elif column == 'area_max':
                conditions.append("CAST(area AS REAL) <= ?")
                params.append(float(value))
            # Фильтры по стоимости
            elif column == 'cost_min':
                conditions.append("CAST(cadastral_cost AS REAL) >= ?")
                params.append(float(value))
            elif column == 'cost_max':
                conditions.append("CAST(cadastral_cost AS REAL) <= ?")
                params.append(float(value))
            elif column == 'cost_exact':
                conditions.append("CAST(cadastral_cost AS REAL) = ?")
                params.append(float(value))
            else:
                conditions.append(f"{column} LIKE ?")
                params.append(f"%{value.strip()}%")
    
    if conditions:
        return " WHERE " + " AND ".join(conditions), params
    return "", []

def ensure_district_table():
    """Создать таблицу сопоставлений районов, если не существует"""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS district_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_name TEXT NOT NULL,
            quarter_code TEXT NOT NULL UNIQUE,
            district_name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def sync_district_mappings():
    """
    Синхронизировать таблицу district_mappings с актуальными данными из land_records.
    Создает записи для новых комбинаций регион/квартал/район, если их нет.
    """
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT 
            COALESCE(region, 'Не указан') AS region_name,
            substr(cadastral_number, 1, instr(cadastral_number, ':') - 1) AS region_code,
            district_code,
            COALESCE(district, 'Не указан') AS district_name
        FROM land_records
        WHERE district_code IS NOT NULL AND district_code != ''
        GROUP BY region_name, region_code, district_code, district_name
    """).fetchall()
    
    for row in rows:
        quarter_code = f"{row['region_code']}:{row['district_code']}"
        conn.execute("""
            INSERT OR IGNORE INTO district_mappings (region_name, quarter_code, district_name)
            VALUES (?, ?, ?)
        """, (row['region_name'], quarter_code, row['district_name']))
    conn.commit()
    conn.close()

def validate_quarter_code(code: str) -> bool:
    """Проверка формата кадастрового квартала (например 16:06)"""
    return bool(re.fullmatch(r"\d{2}:\d{2}", code or ""))

# Инициализируем справочник районов при запуске приложения
ensure_district_table()
sync_district_mappings()

@app.route('/')
def index():
    """Главная страница с таблицей"""
    # Получаем параметры фильтрации и пагинации
    page = request.args.get('page', 1, type=int)
    
    filters = {
        'cadastral_number': request.args.get('filter_cadastral', ''),
        'address': request.args.get('filter_address', ''),
        'district': request.args.get('filter_district', ''),
        'region': request.args.get('filter_region', ''),
        'submission_status': request.args.get('filter_status', ''),
        'land_category': request.args.get('filter_category', ''),
    }
    
    # Специальная обработка для application_number
    app_number_filter = request.args.get('filter_app_number', '')
    app_number_text = request.args.get('filter_app_number_text', '')
    
    if app_number_filter == 'SEARCH' and app_number_text:
        # Если выбран поиск и введён текст - ищем по тексту
        filters['application_number'] = app_number_text
    elif app_number_filter in ['NOT_EMPTY', 'EMPTY']:
        # Если выбрано "Есть номер" или "Пустые"
        filters['application_number'] = app_number_filter
    
    # Фильтр по ID
    if request.args.get('filter_id'):
        filters['id'] = request.args.get('filter_id')
    
    # Фильтр по дате отправки (диапазон от-до)
    if request.args.get('filter_date_from'):
        filters['date_from'] = request.args.get('filter_date_from')
    if request.args.get('filter_date_to'):
        filters['date_to'] = request.args.get('filter_date_to')
    
    # Фильтр по площади (диапазон)
    if request.args.get('filter_area_min'):
        filters['area_min'] = request.args.get('filter_area_min')
    if request.args.get('filter_area_max'):
        filters['area_max'] = request.args.get('filter_area_max')

    # Фильтр по стоимости
    if request.args.get('filter_cost_min'):
        filters['cost_min'] = request.args.get('filter_cost_min')
    if request.args.get('filter_cost_max'):
        filters['cost_max'] = request.args.get('filter_cost_max')
    if request.args.get('filter_cost_exact'):
        filters['cost_exact'] = request.args.get('filter_cost_exact')
    
    # Сортировка
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Валидация сортировки
    valid_sort_columns = ['id', 'cadastral_number', 'address', 'district', 'region', 'submission_status', 
                         'submission_datetime', 'land_category', 'area', 'cadastral_cost', 'application_number']
    
    if sort_by not in valid_sort_columns:
        sort_by = 'id'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'

    # Очищаем пустые фильтры
    filters = {k: v for k, v in filters.items() if v}
    
    conn = get_db_connection()
    
    # Строим запрос с фильтрами
    where_clause, params = build_filter_query(filters)
    
    # Считаем общее количество записей
    count_query = f"SELECT COUNT(*) as total FROM land_records {where_clause}"
    total_items = conn.execute(count_query, params).fetchone()['total']
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    # Получаем записи для текущей страницы
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Определяем сортировку для SQL
    order_clause = f"ORDER BY {sort_by} {sort_order.upper()}"
    
    # Для корректной сортировки чисел и NULL
    if sort_by in ['area', 'cadastral_cost']:
         order_clause = f"ORDER BY CAST({sort_by} AS REAL) {sort_order.upper()}"
    
    query = f"""
        SELECT 
            id,
            cadastral_number,
            address,
            district,
            region,
            submission_status,
            submission_datetime,
            land_category,
            permitted_use,
            area,
            district_code,
            application_number,
            cadastral_cost
        FROM land_records
        {where_clause}
        {order_clause}
        LIMIT ? OFFSET ?
    """
    
    records = conn.execute(query, params + [ITEMS_PER_PAGE, offset]).fetchall()
    
    # Получаем уникальные значения для фильтров
    districts = conn.execute("""
        SELECT DISTINCT district FROM land_records 
        WHERE district IS NOT NULL AND district != ''
        ORDER BY district
    """).fetchall()
    
    regions = conn.execute("""
        SELECT DISTINCT region FROM land_records 
        WHERE region IS NOT NULL AND region != ''
        ORDER BY region
    """).fetchall()
    
    statuses = conn.execute("""
        SELECT DISTINCT submission_status FROM land_records 
        WHERE submission_status IS NOT NULL AND submission_status != ''
        ORDER BY submission_status
    """).fetchall()
    
    categories = conn.execute("""
        SELECT DISTINCT land_category FROM land_records 
        WHERE land_category IS NOT NULL AND land_category != ''
        ORDER BY land_category
        LIMIT 100
    """).fetchall()
    
    # Получаем статистику по статусам
    status_stats = conn.execute("""
        SELECT 
            COALESCE(submission_status, 'Не отправлена') as status,
            COUNT(*) as count
        FROM land_records
        GROUP BY submission_status
        ORDER BY count DESC
    """).fetchall()
    
    conn.close()
    
    # Вычисляем диапазон страниц для пагинации
    page_range_start = max(1, page - 2)
    page_range_end = min(total_pages + 1, page + 3)
    
    # Собираем все параметры запроса для передачи в шаблон (для пагинации)
    query_params = {}
    for key in request.args:
        if key != 'page':  # Исключаем page, он будет добавляться отдельно
            query_params[key] = request.args.get(key)
    
    return render_template('admin.html',
                         records=records,
                         page=page,
                         total_pages=total_pages,
                         total_items=total_items,
                         filters=filters,
                         query_params=query_params,
                         districts=[d['district'] for d in districts],
                         regions=[r['region'] for r in regions],
                         statuses=[s['submission_status'] for s in statuses],
                         categories=[c['land_category'] for c in categories],
                         status_stats=status_stats,
                         items_per_page=ITEMS_PER_PAGE,
                         page_range_start=page_range_start,
                         page_range_end=page_range_end,
                         sort_by=sort_by,
                         sort_order=sort_order)

@app.route('/api/statistics')
def statistics():
    """API для получения статистики"""
    conn = get_db_connection()
    
    # Общая статистика
    total = conn.execute('SELECT COUNT(*) as count FROM land_records').fetchone()['count']
    
    statuses = conn.execute('''
        SELECT 
            COALESCE(submission_status, 'Не отправлена') as status,
            COUNT(*) as count
        FROM land_records
        GROUP BY submission_status
    ''').fetchall()
    
    # По регионам
    regions = conn.execute('''
        SELECT region, COUNT(*) as count
        FROM land_records
        WHERE region IS NOT NULL
        GROUP BY region
        ORDER BY count DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'total': total,
        'by_status': [dict(row) for row in statuses],
        'by_region': [dict(row) for row in regions]
    })

@app.route('/api/update_status/<int:record_id>', methods=['POST'])
def update_status(record_id):
    """Обновить статус записи"""
    data = request.json
    new_status = data.get('status')
    
    conn = get_db_connection()
    
    if new_status == 'Отправлено':
        conn.execute('''
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?
            WHERE id = ?
        ''', (new_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record_id))
    else:
        conn.execute('''
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = NULL
            WHERE id = ?
        ''', (new_status, record_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/bulk_update_status', methods=['POST'])
def bulk_update_status():
    """Массовое обновление статусов"""
    data = request.json
    new_status = data.get('status')
    filters = data.get('filters', {})
    
    if not new_status:
        return jsonify({'success': False, 'message': 'Статус не указан'}), 400
    
    # Строим WHERE clause из фильтров
    where_clause, params = build_filter_query(filters)
    
    conn = get_db_connection()
    
    # Сначала считаем количество записей, которые будут обновлены
    count_query = f"SELECT COUNT(*) as total FROM land_records {where_clause}"
    count = conn.execute(count_query, params).fetchone()['total']
    
    if count == 0:
        conn.close()
        return jsonify({'success': False, 'message': 'Нет записей для обновления'}), 400
    
    # Обновляем статусы
    if new_status == 'Отправлено':
        update_query = f"""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?
            {where_clause.replace('WHERE', 'WHERE', 1) if where_clause else ''}
        """
        conn.execute(update_query, [new_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + params)
    else:
        update_query = f"""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = NULL
            {where_clause.replace('WHERE', 'WHERE', 1) if where_clause else ''}
        """
        conn.execute(update_query, [new_status] + params)
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'count': count, 'message': f'Обновлено записей: {count}'})

@app.route('/api/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """Удалить запись"""
    conn = get_db_connection()
    conn.execute('DELETE FROM land_records WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/districts')
def districts_page():
    """Страница редактирования районов"""
    conn = get_db_connection()
    districts_rows = conn.execute("""
        SELECT id, region_name, quarter_code, district_name, responsible_org, org_address, email, phone
        FROM district_mappings
        ORDER BY quarter_code
    """).fetchall()
    conn.close()
    
    # Преобразуем Row объекты в обычные словари для JSON сериализации
    districts = [dict(row) for row in districts_rows]
    
    return render_template('districts.html', districts=districts)

@app.route('/api/districts', methods=['POST'])
def create_district_mapping():
    """Создать новый район"""
    data = request.json or {}
    region_name = (data.get('region') or '').strip()
    quarter_code = (data.get('quarter') or '').strip()
    district_name = (data.get('district') or '').strip()
    
    if not region_name or not district_name or not validate_quarter_code(quarter_code):
        return jsonify({'success': False, 'message': 'Некорректные данные'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO district_mappings (region_name, quarter_code, district_name)
            VALUES (?, ?, ?)
        """, (region_name, quarter_code, district_name))
        conn.commit()
        new_id = conn.execute("SELECT last_insert_rowid() as id").fetchone()['id']
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Такой квартал уже существует'}), 400
    
    row = conn.execute("""
        SELECT id, region_name, quarter_code, district_name
        FROM district_mappings WHERE id = ?
    """, (new_id,)).fetchone()
    conn.close()
    return jsonify({'success': True, 'district': dict(row)})

@app.route('/api/districts/<int:mapping_id>', methods=['POST'])
def update_district_mapping(mapping_id):
    """Обновить существующий район"""
    data = request.json or {}
    region_name = (data.get('region') or '').strip()
    quarter_code = (data.get('quarter') or '').strip()
    district_name = (data.get('district') or '').strip()
    responsible_org = (data.get('responsible_org') or '').strip()
    org_address = (data.get('org_address') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    
    if not region_name or not district_name or not validate_quarter_code(quarter_code):
        return jsonify({'success': False, 'message': 'Некорректные данные'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE district_mappings
            SET region_name = ?, quarter_code = ?, district_name = ?, 
                responsible_org = ?, org_address = ?, email = ?, phone = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (region_name, quarter_code, district_name, responsible_org, org_address, email, phone, mapping_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Квартал уже используется'}), 400
    
    row = conn.execute("""
        SELECT id, region_name, quarter_code, district_name, responsible_org, org_address, email, phone
        FROM district_mappings WHERE id = ?
    """, (mapping_id,)).fetchone()
    conn.close()
    return jsonify({'success': True, 'district': dict(row)})

def get_bot_status():
    """Проверить статус бота"""
    global BOT_PROCESS
    if BOT_PROCESS and BOT_PROCESS.poll() is None:
        return {'running': True, 'pid': BOT_PROCESS.pid}
    # Проверяем через ps
    try:
        result = subprocess.run(['pgrep', '-f', 'auto_submit.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pid = int(result.stdout.strip().split('\n')[0])
            return {'running': True, 'pid': pid}
    except:
        pass
    return {'running': False}

def load_bot_config():
    """Загрузить настройки бота"""
    if os.path.exists(BOT_CONFIG_FILE):
        try:
            with open(BOT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        'regions': [],
        'cost_min': 0,
        'cost_max': None
    }

def save_bot_config(config):
    """Сохранить настройки бота"""
    with open(BOT_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@app.route('/bot')
def bot_control_page():
    """Страница управления ботом"""
    status = get_bot_status()
    config = load_bot_config()
    
    # Получаем доступные регионы
    conn = get_db_connection()
    regions = conn.execute("""
        SELECT DISTINCT substr(cadastral_number, 1, instr(cadastral_number || ':', ':') - 1) as code,
               region
        FROM land_records
        WHERE region IS NOT NULL AND region != ''
        GROUP BY code, region
        ORDER BY code
    """).fetchall()
    conn.close()
    
    return render_template('bot_control.html', 
                         bot_status=status,
                         bot_config=config,
                         available_regions=[dict(r) for r in regions])

@app.route('/api/bot/status')
def bot_status():
    """API: статус бота"""
    return jsonify(get_bot_status())

@app.route('/api/bot/start', methods=['POST'])
def bot_start():
    """API: запустить бота"""
    global BOT_PROCESS
    
    status = get_bot_status()
    if status['running']:
        return jsonify({'success': False, 'message': 'Бот уже запущен'}), 400
    
    try:
        config = load_bot_config()
        # Запускаем бота с настройками и DISPLAY для виртуального дисплея
        env = os.environ.copy()
        env['DISPLAY'] = ':99'
        BOT_PROCESS = subprocess.Popen(
            ['python3', 'auto_submit.py'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=open('bot.log', 'a'),
            stderr=open('bot.err', 'a'),
            env=env
        )
        return jsonify({'success': True, 'pid': BOT_PROCESS.pid})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def bot_stop():
    """API: остановить бота"""
    global BOT_PROCESS
    
    try:
        # Останавливаем через pkill
        subprocess.run(['pkill', '-f', 'auto_submit.py'], check=False)
        if BOT_PROCESS:
            BOT_PROCESS.terminate()
            BOT_PROCESS = None
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bot/config', methods=['GET'])
def get_bot_config():
    """API: получить настройки бота"""
    return jsonify(load_bot_config())

@app.route('/api/bot/config', methods=['POST'])
def save_bot_config_api():
    """API: сохранить настройки бота"""
    data = request.json or {}
    config = {
        'regions': data.get('regions', []),
        'cost_min': data.get('cost_min', 0),
        'cost_max': data.get('cost_max')
    }
    save_bot_config(config)
    return jsonify({'success': True, 'config': config})

@app.route('/api/bot/sms', methods=['POST'])
def submit_sms_code():
    """API: отправить SMS код"""
    data = request.json or {}
    sms_code = data.get('code', '').strip()
    
    if not sms_code:
        return jsonify({'success': False, 'message': 'Код не указан'}), 400
    
    try:
        with open(SMS_CODE_FILE, 'w', encoding='utf-8') as f:
            f.write(sms_code)
        return jsonify({'success': True, 'message': 'SMS код отправлен боту'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bot/logs')
def bot_logs():
    """API: получить логи бота"""
    try:
        with open('bot.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Последние 100 строк
            return jsonify({'logs': ''.join(lines[-100:])})
    except:
        return jsonify({'logs': 'Логи не найдены'})

@app.route('/bot/screen')
def bot_screen_page():
    """Страница просмотра экрана бота"""
    return render_template('bot_screen.html')

@app.route('/api/bot/screenshot')
def get_last_screenshot():
    """API: получить последний скриншот"""
    import base64
    screenshots_dir = 'screenshots'
    
    try:
        # Читаем путь к последнему скриншоту
        last_file = os.path.join(screenshots_dir, 'last_screenshot.txt')
        if os.path.exists(last_file):
            with open(last_file, 'r') as f:
                screenshot_path = f.read().strip()
            
            if os.path.exists(screenshot_path):
                # Читаем изображение и кодируем в base64
                with open(screenshot_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                return jsonify({
                    'success': True,
                    'image': f'data:image/png;base64,{img_data}',
                    'timestamp': os.path.getmtime(screenshot_path)
                })
        
        # Если нет последнего, ищем любой скриншот
        if os.path.exists(screenshots_dir):
            screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
            if screenshots:
                screenshots.sort(reverse=True)
                latest = os.path.join(screenshots_dir, screenshots[0])
                with open(latest, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                return jsonify({
                    'success': True,
                    'image': f'data:image/png;base64,{img_data}',
                    'timestamp': os.path.getmtime(latest)
                })
        
        return jsonify({'success': False, 'message': 'Скриншоты не найдены'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bot/screenshots/list')
def list_screenshots():
    """API: список всех скриншотов"""
    screenshots_dir = 'screenshots'
    screenshots = []
    
    try:
        if os.path.exists(screenshots_dir):
            for f in os.listdir(screenshots_dir):
                if f.endswith('.png'):
                    path = os.path.join(screenshots_dir, f)
                    screenshots.append({
                        'filename': f,
                        'path': f'/screenshots/{f}',
                        'timestamp': os.path.getmtime(path),
                        'size': os.path.getsize(path)
                    })
            screenshots.sort(key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        pass
    
    return jsonify({'screenshots': screenshots[:50]})  # Последние 50

@app.route('/screenshots/<filename>')
def serve_screenshot(filename):
    """Отдать скриншот"""
    return send_from_directory('screenshots', filename)

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 Запуск веб-админки...")
    print("=" * 80)
    print("\n📊 Откройте в браузере: http://127.0.0.1:5001")
    print("⚠️  Нажмите Ctrl+C для остановки\n")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5001)

