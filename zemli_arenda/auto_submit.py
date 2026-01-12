#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическая отправка заявлений на аренду земельных участков через Госуслуги
"""

import time
import logging
import sqlite3
import os
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gosuslugi_auto.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DB_PATH = "land_records.db"

# Справочник кодов районов Челябинской области
DISTRICT_CODES = {
    "00": "Новогорный",
    "01": "Агаповский",
    "02": "Аргаяшский",
    "03": "Ашинский",
    "04": "Брединский",
    "05": "Варненский",
    "06": "Верхнеуральский",
    "07": "Еткульский",
    "08": "Карталинский",
    "09": "Каслинский",
    "10": "Катав-Ивановский",
    "11": "Кизильский",
    "12": "Красноармейский",
    "13": "Кунашакский",
    "14": "Кусинский",
    "15": "Нагайбакский",
    "16": "Нязепетровский",
    "17": "Октябрьский",
    "18": "Саткинский",
    "19": "Сосновский",
    "20": "Троицкий",
    "21": "Увельский",
    "22": "Уйский",
    "23": "Чебаркульский",
    "24": "Чесменский",
    "25": "Златоуст",
    "26": "Пластовский",
    "27": "Верхний Уфалей",
    "28": "Еманжелинский",
    "29": "Карабаш",
    "30": "Копейск",
    "31": "Коркино",
    "32": "Кыштым",
    "33": "Магнитогорск",
    "34": "Миасс",
    "35": "Троицк",
    "36": "Челябинск",
    "37": "Южноуральск",
    "38": "Чебаркуль",
    "39": "Усть-Катав",
    "40": "Снежинск",
    "41": "Озерск",
    "42": "Трехгорный",
}

def get_district_name_by_cadastral(cadastral_number):
    """Получить название района по кадастровому номеру"""
    try:
        parts = cadastral_number.split(':')
        if len(parts) >= 2:
            code = parts[1]
            return DISTRICT_CODES.get(code, code)
    except:
        pass
    return None

def get_responsible_org_by_cadastral(cadastral_number):
    """
    Получить ответственный орган из district_mappings по кадастровому номеру.
    
    Args:
        cadastral_number: Кадастровый номер (например, 74:29:0101001:123)
    
    Returns:
        str: Полное название ответственного органа или None
    """
    try:
        parts = cadastral_number.strip().split(':')
        if len(parts) >= 2:
            # Формируем код квартала (например, 74:29)
            quarter_code = f"{parts[0]}:{parts[1]}"
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT responsible_org
                FROM district_mappings
                WHERE quarter_code = ?
            """, (quarter_code,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0]:
                return row[0].strip()
            
            logger.warning(f"⚠️ Ответственный орган не найден для квартала {quarter_code}")
            return None
    except Exception as e:
        logger.error(f"❌ Ошибка получения ответственного органа: {e}")
        return None

def get_db_connection():
    """Подключение к БД"""
    return sqlite3.connect(DB_PATH)

def get_available_regions():
    """Получить список доступных регионов из БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT SUBSTR(cadastral_number, 1, 2) as region_code
        FROM land_records
        WHERE cadastral_number IS NOT NULL
          AND (submission_status IS NULL OR submission_status = '' OR submission_status = 'Не отправлена' 
               OR submission_status = 'Ошибка' OR submission_status = 'Не найден на Росреестре')
        ORDER BY region_code
    """)
    
    regions = [row[0] for row in cursor.fetchall()]
    
    # Получаем статистику по каждому region
    region_stats = {}
    for region in regions:
        cursor.execute("""
            SELECT COUNT(*)
            FROM land_records
            WHERE cadastral_number LIKE ?
              AND (submission_status IS NULL OR submission_status = '' OR submission_status = 'Не отправлена'
                   OR submission_status = 'Ошибка' OR submission_status = 'Не найден на Росреестре')
        """, (f"{region}:%",))
        count = cursor.fetchone()[0]
        region_stats[region] = count
    
    conn.close()
    return region_stats

def ask_for_regions():
    """Запросить у пользователя коды регионов"""
    print("\n" + "="*80)
    print("🌍 ВЫБОР РЕГИОНОВ ДЛЯ ОТПРАВКИ ЗАЯВЛЕНИЙ")
    print("="*80)
    
    # Получаем доступные регионы
    region_stats = get_available_regions()
    
    if not region_stats:
        print("\n❌ Нет доступных регионов для отправки!")
        return None
    
    print("\n📊 Доступные регионы (неотправленные заявки):\n")
    for region_code, count in sorted(region_stats.items()):
        print(f"   {region_code}: {count:,} заявок".replace(',', ' '))
    
    print("\n" + "-"*80)
    print("💡 Введите коды регионов через запятую (например: 74,66,77)")
    print("   Или нажмите Enter для отправки по ВСЕМ регионам")
    print("-"*80)
    
    user_input = input("\n👉 Ваш выбор: ").strip()
    
    if not user_input:
        print("\n✅ Выбраны ВСЕ регионы")
        return None  # None означает все регионы
    
    # Парсим ввод
    try:
        selected_regions = [code.strip() for code in user_input.split(',')]
        
        # Валидация
        invalid = [r for r in selected_regions if r not in region_stats]
        if invalid:
            print(f"\n⚠️ Неверные коды регионов: {', '.join(invalid)}")
            print("Попробуйте снова...")
            return ask_for_regions()  # Рекурсивный вызов
        
        # Показываем выбранные регионы
        print(f"\n✅ Выбраны регионы: {', '.join(selected_regions)}")
        total = sum(region_stats[r] for r in selected_regions)
        print(f"📊 Всего заявок: {total:,}".replace(',', ' '))
        
        return selected_regions
    except Exception as e:
        print(f"\n❌ Ошибка ввода: {e}")
        return ask_for_regions()  # Рекурсивный вызов

def get_parcels_to_submit(region_codes=None):
    """
    Получить участки для отправки из указанных регионов.
    
    Args:
        region_codes: Список кодов регионов (например, ['74', '66']) или None для всех
    
    Returns:
        List[(id, cadastral_number, address, district, district_code)]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Формируем условие для фильтрации по регионам
    if region_codes:
        region_conditions = " OR ".join([f"cadastral_number LIKE '{code}:%'" for code in region_codes])
        where_region = f"AND ({region_conditions})"
    else:
        where_region = ""
    
    # Получаем список всех кодов районов из выбранных регионов (не отправленных)
    query = f"""
        SELECT DISTINCT district_code 
        FROM land_records 
        WHERE 1=1
          {where_region}
          AND district_code IS NOT NULL
          AND (submission_status IS NULL OR submission_status = '' OR submission_status = 'Не отправлена'
               OR submission_status = 'Ошибка' OR submission_status = 'Не найден на Росреестре')
        ORDER BY district_code
    """
    
    cursor.execute(query)
    district_codes = [row[0] for row in cursor.fetchall()]
    
    logger.info(f"📊 Найдено районов: {len(district_codes)}")
    
    # Для каждого района получаем ВСЕ участки (без ограничения)
    parcels_by_district = {}
    for district_code in district_codes:
        query = f"""
            SELECT id, cadastral_number, address, district, district_code
            FROM land_records 
            WHERE 1=1
              {where_region}
              AND district_code = ?
              AND (submission_status IS NULL OR submission_status = '' OR submission_status = 'Не отправлена'
                   OR submission_status = 'Ошибка' OR submission_status = 'Не найден на Росреестре')
            ORDER BY id
        """
        
        cursor.execute(query, (district_code,))
        parcels = cursor.fetchall()
        if parcels:
            parcels_by_district[district_code] = parcels
    
    conn.close()
    
    # Чередуем участки: берём по 1 из каждого района по кругу
    parcels_to_submit = []
    max_parcels = max(len(p) for p in parcels_by_district.values()) if parcels_by_district else 0
    
    for round_num in range(max_parcels):
        for district_code in district_codes:
            if district_code in parcels_by_district:
                parcels = parcels_by_district[district_code]
                if round_num < len(parcels):
                    parcels_to_submit.append(parcels[round_num])
    
    logger.info(f"✅ Подготовлено заявок: {len(parcels_to_submit)}")
    return parcels_to_submit

def update_parcel_status(parcel_id, status, error_message=None, application_number=None, encumbrances=None):
    """Обновить статус участка в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    msk_tz = pytz.timezone('Europe/Moscow')
    now_msk = datetime.now(msk_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    if encumbrances:
        # Если есть обременения - сохраняем их
        cursor.execute("""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?, encumbrances = ?
            WHERE id = ?
        """, (status, now_msk, encumbrances, parcel_id))
    elif error_message:
        notes = f"Ошибка: {error_message}"
        cursor.execute("""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?, notes = ?
            WHERE id = ?
        """, (status, now_msk, notes, parcel_id))
    elif application_number:
        # Если есть номер заявления - сохраняем его
        cursor.execute("""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?, application_number = ?
            WHERE id = ?
        """, (status, now_msk, application_number, parcel_id))
    else:
        cursor.execute("""
            UPDATE land_records 
            SET submission_status = ?, submission_datetime = ?
            WHERE id = ?
        """, (status, now_msk, parcel_id))
    
    conn.commit()
    conn.close()

def check_encumbrances_rosreestr(driver, wait, cadastral_number):
    """
    Проверить обременения на Росреестре
    
    Returns:
        tuple: (success, encumbrances_text)
        - success: True если проверка прошла успешно
        - encumbrances_text: Текст ошибки/занятости или None если свободно
    """
    try:
        logger.info(f"🔍 Проверка обременений для {cadastral_number} на Росреестре...")
        
        # ВСЕГДА переходим на страницу поиска (НЕ refresh, а GET!)
        rosreestr_url = "https://lk.rosreestr.ru/eservices/real-estate-objects-online"
        
        logger.info(f"   🔄 Переход на страницу поиска...")
        driver.get(rosreestr_url)
        
        # Ждём загрузки страницы
        logger.info("   ⏳ Ожидание загрузки страницы (10 секунд)...")
        time.sleep(10)
        
        # Проверяем, что мы на правильной странице
        current_url = driver.current_url
        if "real-estate-objects-online" not in current_url:
            logger.error(f"   ❌ Неправильный URL: {current_url}")
            raise Exception(f"Не удалось перейти на страницу поиска. Текущий URL: {current_url}")
        
        logger.info(f"   ✅ Страница загружена: {current_url[:80]}...")
        
        # Проверяем готовность DOM
        ready_state = driver.execute_script("return document.readyState")
        if ready_state != 'complete':
            logger.warning(f"   ⚠️ DOM не готов (readyState: {ready_state}), жду ещё 3 сек...")
            time.sleep(3)
        
        # ПРОВЕРЯЕМ АВТОРИЗАЦИЮ - может кнопка "Войти" есть
        logger.info("   🔍 Проверка авторизации...")
        try:
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')] | //a[contains(text(), 'Войти')]")
            logger.warning("   ⚠️  Обнаружена кнопка 'Войти' - выполняю авторизацию!")
            logger.info("   🔑 Клик на 'Войти'...")
            login_button.click()
            time.sleep(3)
            logger.info("   ✅ Авторизация выполнена")
            
            # Возвращаемся на страницу поиска после логина
            logger.info("   🔄 Возврат на страницу поиска...")
            driver.get(rosreestr_url)
            time.sleep(3)
        except:
            logger.info("   ✅ Уже авторизован (кнопка 'Войти' не найдена)")
        
        # Ждём появления dropdown "Вид объекта" (React должен отрендерить форму)
        logger.info("   ⏳ Ожидание появления dropdown 'Вид объекта'...")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rros-ui-lib-dropdown__control')]")))
            logger.info("   ✅ Dropdown 'Вид объекта' найден!")
            time.sleep(1)  # Даём время на полную инициализацию
        except Exception as e:
            logger.warning(f"   ⚠️ Dropdown не найден через XPath, жду ещё 3 сек: {e}")
            time.sleep(3)
        
        # Шаг 1: КЛИК ПО КООРДИНАТАМ РЯДОМ С ТЕКСТОМ "Вид объекта"
        logger.info("   📝 Шаг 1: Поиск текста 'Вид объекта' и клик рядом...")
        try:
            # Ищем ЛЮБОЙ видимый элемент с текстом "Вид объекта"
            label_xpath = "//*[contains(text(), 'Вид объекта') and not(self::script) and not(self::style)]"
            
            # Ждём появления
            try:
                label = wait.until(EC.visibility_of_element_located((By.XPATH, label_xpath)))
            except:
                # Если не нашли видимый, ищем любой в DOM
                label = driver.find_element(By.XPATH, label_xpath)
            
            logger.info(f"   ✅ Нашел элемент с текстом: {label.tag_name}")
            
            # Скроллим к нему
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            time.sleep(0.5)
            
            # Получаем координаты через JS (надежнее)
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", label)
            
            # Вычисляем координаты клика (справа от текста)
            # rect.right + 150px, rect.top + height/2
            click_x = rect['right'] + 150
            click_y = rect['top'] + (rect['height'] / 2)
            
            logger.info(f"   📍 Координаты клика (viewport): x={click_x}, y={click_y}")
            
            # Кликаем по координатам через JS (MouseEvent)
            driver.execute_script(f"""
                var x = {click_x};
                var y = {click_y};
                var el = document.elementFromPoint(x, y);
                
                if (el) {{
                    console.log('Clicking on:', el);
                    el.click();
                    
                    // Дополнительно шлем события мыши
                    ['mousedown', 'mouseup', 'click'].forEach(function(type) {{
                        var evt = new MouseEvent(type, {{
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: x,
                            clientY: y,
                            button: 0
                        }});
                        el.dispatchEvent(evt);
                    }});
                }}
            """)
            
            logger.info("   ✅ Клик выполнен!")
            time.sleep(2)  # Ждём открытия dropdown
            
            # Вместо поиска input - СРАЗУ ИЩЕМ ОПЦИЮ "Земельный участок"
            logger.info("   🔍 Ищу опцию 'Земельный участок' в открытом списке...")
            
            try:
                # Ищем элемент с текстом "Земельный участок"
                option_xpath = "//*[text()='Земельный участок' and not(self::input)]"
                
                # Ждём появления (увеличил таймаут до 5 сек)
                option = wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
                
                logger.info("   ✅ Опция найдена!")
                
                # Кликаем по опции
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                time.sleep(0.3)
                option.click()
                
                logger.info("   ✅ Опция 'Земельный участок' выбрана!")
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"   ⚠️ Опция не найдена стандартно: {e}")
                
                # Запасной вариант: ищем через JS
                logger.info("   🔄 Пробую найти через JS...")
                js_click_option = """
                var all = document.querySelectorAll('*');
                for (var i=0; i<all.length; i++) {
                    if (all[i].innerText === 'Земельный участок' && all[i].offsetWidth > 0) {
                        all[i].click();
                        return true;
                    }
                }
                return false;
                """
                if driver.execute_script(js_click_option):
                    logger.info("   ✅ Опция выбрана через JS!")
                else:
                    raise Exception("Не удалось выбрать опцию 'Земельный участок'")
            
        except Exception as e:
            logger.error(f"   ❌ Не удалось выбрать тип объекта: {e}")
            screenshot_path = f"rosreestr_dropdown_error_{cadastral_number.replace(':', '_')}.png"
            driver.save_screenshot(screenshot_path)
            logger.error(f"   📸 Скриншот сохранён: {screenshot_path}")
            import traceback
            traceback.print_exc()
            return False, None
        
        # Шаг 2: Ввести кадастровый номер
        logger.info(f"   📝 Шаг 2: Ввод кадастрового номера {cadastral_number}...")
        try:
            # Ищем поле по id="query"
            cadastral_input_xpaths = [
                "//input[@id='query']",
                "//input[@name='query']",
                "//input[@placeholder='Введите адрес или кадастровый номер объекта']"
            ]
            
            input_found = False
            for xpath in cadastral_input_xpaths:
                try:
                    logger.info(f"   🔍 Пробую XPath: {xpath[:60]}...")
                    cadastral_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    logger.info("   ✅ Найдено поле ввода кадастра")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cadastral_input)
                    time.sleep(0.3)
                    
                    cadastral_input.clear()
                    cadastral_input.send_keys(cadastral_number)
                    logger.info(f"   ✅ Введён кадастровый номер: {cadastral_number}")
                    input_found = True
                    time.sleep(1)
                    break
                except Exception as e:
                    logger.debug(f"   ⚠️ Не сработало: {str(e)[:50]}")
                    continue
            
            if not input_found:
                raise Exception("Не удалось найти поле ввода кадастрового номера")
                
        except Exception as e:
            logger.error(f"   ❌ Не удалось ввести кадастровый номер: {e}")
            screenshot_path = f"rosreestr_input_error_{cadastral_number.replace(':', '_')}.png"
            driver.save_screenshot(screenshot_path)
            logger.error(f"   📸 Скриншот сохранён: {screenshot_path}")
            return False, None
        
        # Шаг 2.5: Ввести капчу (символы с картинки)
        logger.info("   📝 Шаг 2.5: Проверка наличия капчи...")
        try:
            # Ищем поле для капчи
            captcha_input = driver.find_element(By.XPATH, "//label[contains(text(), 'Введите символы с картинки')]/following-sibling::*//input")
            logger.warning("   ⚠️  ОБНАРУЖЕНА КАПЧА!")
            logger.info("   ⏸️  Пожалуйста, введите символы с картинки вручную в браузере")
            logger.info("   ⏳ Ожидание 60 секунд для ручного ввода капчи...")
            time.sleep(60)
        except:
            logger.info("   ✅ Капча не обнаружена")
        
        # Шаг 3: Нажать кнопку "Найти"
        logger.info("   📝 Шаг 3: Нажатие кнопки 'Найти'...")
        try:
            search_button = None
            
            # ВАРИАНТ 0: Поиск по ID (самый надежный!)
            try:
                search_button = driver.find_element(By.ID, "realestateobjects-search")
                logger.info("   ✅ Найдена кнопка по ID: realestateobjects-search")
            except:
                pass
            
            # ВАРИАНТ 1: Поиск по тексту (любой регистр, любой тег)
            if not search_button:
                logger.info("   🔍 Ищу элемент с текстом 'Найти'/'НАЙТИ'...")
            
            xpath_text = "//*[contains(text(), 'Найти') or contains(text(), 'НАЙТИ')]"
            elements = driver.find_elements(By.XPATH, xpath_text)
            
            for el in elements:
                if el.is_displayed() and el.size['width'] > 0:
                    # Проверяем, что это не label и не title
                    tag = el.tag_name.lower()
                    if tag not in ['script', 'style', 'meta', 'link', 'title']:
                        search_button = el
                        logger.info(f"   ✅ Найдена кнопка по тексту! (Тег: {tag})")
                        break
            
            # ВАРИАНТ 2: Поиск по CSS классу (если текст не сработал)
            if not search_button:
                logger.info("   🔍 Ищу по CSS классам...")
                try:
                    search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    logger.info("   ✅ Найдена кнопка type='submit'")
                except:
                    try:
                        search_button = driver.find_element(By.CSS_SELECTOR, ".search-button, .btn-search")
                        logger.info("   ✅ Найдена кнопка по классу search")
                    except:
                        pass

            if search_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
                time.sleep(0.5)
                
                # Кликаем JS (самый надежный способ для таких кнопок)
                driver.execute_script("arguments[0].click();", search_button)
                logger.info("   ✅ Нажата кнопка 'Найти' (JS)")
                time.sleep(5)
            else:
                logger.error("   ❌ Кнопка 'Найти' вообще не найдена!")
                driver.save_screenshot(f"rosreestr_no_search_btn_{cadastral_number.replace(':', '_')}.png")
                # Не выходим, пробуем нажать Enter в поле ввода!
                logger.info("   ⚠️ Пробую нажать ENTER в поле ввода...")
                if 'cadastral_input' in locals():
                    cadastral_input.send_keys(Keys.ENTER)
                    time.sleep(5)
                else:
                    return False, None

        except Exception as e:
            logger.error(f"   ❌ Ошибка с кнопкой 'Найти': {e}")
            driver.save_screenshot(f"rosreestr_search_error_{cadastral_number.replace(':', '_')}.png")
            return False, None
        
        # Шаг 4: Найти и кликнуть на результат с кадастровым номером
        logger.info("   📝 Шаг 4: Поиск результата с кадастровым номером...")
        try:
            # Ищем элемент с текстом кадастрового номера (может быть кнопка, ссылка или div)
            result_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{cadastral_number}')] | //a[contains(text(), '{cadastral_number}')] | //div[contains(text(), '{cadastral_number}') and contains(@class, 'clickable')]"))
            )
            logger.info(f"   ✅ Найден результат: {cadastral_number}")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result_element)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", result_element)
            logger.info("   ✅ Кликнули на результат")
            time.sleep(2)  # Ожидание открытия всплывающего окна
        except Exception as e:
            logger.error(f"   ❌ Результат не найден на Росреестре: {e}")
            driver.save_screenshot(f"rosreestr_not_found_{cadastral_number.replace(':', '_')}.png")
            return False, None
        
        # Шаг 5: Поиск обременений во всплывающем окне
        logger.info("   📝 Шаг 5: Анализ данных во всплывающем окне...")
        
        # --- 1. ПОИСК КАДАСТРОВОЙ СТОИМОСТИ ---
        try:
            logger.info("   💰 Ищу кадастровую стоимость...")
            cost_text = None
            
            # Используем короткое ожидание (5 сек) для поиска элемента
            short_wait = WebDriverWait(driver, 5)
            
            try:
                # Попытка 1: Ищем элемент, содержащий текст "Кадастровая стоимость"
                cost_label = short_wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Кадастровая стоимость')]")
                ))
                
                # Пробуем найти значение в соседнем элементе или родительском блоке
                try:
                    cost_element = cost_label.find_element(By.XPATH, "./following-sibling::*[1] | ./../following-sibling::*[1]")
                    cost_text = cost_element.text.strip()
                except:
                    # Если соседа нет, берем текст родительского контейнера
                    cost_text = cost_label.find_element(By.XPATH, "./..").text.strip()
                    
            except Exception:
                # Попытка 2: Если точный текст не найден, ищем по частичному совпадению
                try:
                    cost_label = driver.find_element(By.XPATH, "//*[contains(text(), 'Кадастровая') and contains(text(), 'стоимость')]")
                    cost_text = cost_label.find_element(By.XPATH, "./..").text.strip()
                except:
                    logger.warning("      Не удалось найти элемент 'Кадастровая стоимость' (XPath)")

            if cost_text:
                logger.info(f"      Найдено значение (сырое): {cost_text}")
            
                # Очистка: "236320.84 руб." -> 236320
                import re
                # Ищем число, которое может содержать точку
                match = re.search(r'(\d+[\.,]?\d*)', cost_text.replace(' ', '').replace('\xa0', ''))
                if match:
                    cost_str = match.group(1).replace(',', '.')
                    cost_val = float(cost_str)
                    cost_int = int(cost_val)
                    
                    # Сохраняем в БД
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE land_records SET cadastral_cost = ? WHERE cadastral_number = ?", (cost_int, cadastral_number))
                        conn.commit()
                        conn.close()
                        logger.info(f"   ✅ Кадастровая стоимость сохранена в БД: {cost_int}")
                    except Exception as db_err:
                        logger.error(f"   ❌ Ошибка записи в БД: {db_err}")
                else:
                    logger.warning("      Не удалось распознать число в строке стоимости")
            else:
                logger.warning("      Не удалось найти текст со стоимостью")
                
        except Exception as e:
             logger.warning(f"   ⚠️ Не удалось извлечь кадастровую стоимость: {e}")

        # --- 2. ПРОВЕРКА НА "ЗАНЯТОСТЬ" (ОБРЕМЕНЕНИЯ) ---
        logger.info("   🔒 Проверка на наличие прав и обременений...")
        
        target_phrases = [
            "Сведения о правах и ограничениях (обременениях)",
            "Вид, номер и дата государственной регистрации права",
            "Ограничение прав и обременение объекта недвижимости",
            "Ограничение прав и обременение объекта",
            "Ограничение прав"
        ]
        
        found_encumbrance = False
        found_phrase = ""
        
        for phrase in target_phrases:
            try:
                driver.find_element(By.XPATH, f"//*[contains(text(), '{phrase}')]")
                found_encumbrance = True
                found_phrase = phrase
                logger.info(f"   ⛔️ Найдено: '{phrase}'")
                break
            except:
                pass
                
        if found_encumbrance:
            logger.warning(f"   ⚠️  Участок {cadastral_number}: ЗАНЯТ (найдено '{found_phrase}')")
            # Возвращаем текст, чтобы вызывающий код поставил статус "Занят"
            return True, f"Занят: найдено '{found_phrase}'"
        
        # Если ничего не нашли - значит участок свободен (по мнению скрипта)
        logger.info("   ✅ Обременений/прав не найдено - участок СВОБОДЕН")
        return True, None
        
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке обременений: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"rosreestr_error_{cadastral_number.replace(':', '_')}.png")
        return False, None

def fill_form(driver, wait, cadastral_number):
    """Заполнить форму для одного участка"""
    try:
        # Определяем район по кадастровому номеру
        district = get_district_name_by_cadastral(cadastral_number)
        district_code = cadastral_number.split(':')[1] if ':' in cadastral_number else ''
        
        logger.info(f"🔍 Заполняю форму для {cadastral_number}")
        logger.info(f"   Код района: {district_code}, Название: {district}")
        
        # Переход на страницу услуги (НЕ на главную, чтобы избежать редиректа на старую форму)
        logger.info("Перехожу на страницу услуги...")
        driver.get("https://www.gosuslugi.ru/600231/1/form")
        time.sleep(1.5)
        
        # ВАЖНО: Проверяем, не открыта ли старая форма с order ID
        max_attempts = 3
        for attempt in range(max_attempts):
            current_url = driver.current_url
            page_source = driver.page_source
            
            # Если в URL есть /order/ - значит открылась старая сохраненная форма
            if "/order/" in current_url and "Всё заполнено" in page_source:
                logger.warning(f"⚠️ Попытка {attempt + 1}/{max_attempts}: Обнаружена старая сохраненная форма ({current_url})")
                
                # Пробуем кликнуть "Назад" если есть
                try:
                    back_button = driver.find_element(By.XPATH, "//button[contains(., 'Назад')] | //a[contains(., 'Назад')]")
                    driver.execute_script("arguments[0].click();", back_button)
                    logger.info("   Нажата кнопка 'Назад'")
                    time.sleep(1)
                except:
                    logger.warning("   Кнопка 'Назад' не найдена")
                
                # Принудительно переходим на страницу услуги заново
                driver.get("https://www.gosuslugi.ru/600231/1/form")
                time.sleep(1)
            elif "/order/" not in current_url:
                logger.info(f"✅ Страница услуги открыта корректно: {current_url}")
                break
        else:
            # Если после 3 попыток всё ещё старая форма - делаем жёсткую очистку
            logger.error("❌ Не удалось выйти из старой формы, делаю жёсткую очистку...")
            driver.delete_all_cookies()
            time.sleep(0.5)
            driver.get("https://www.gosuslugi.ru/600231/1/form")
            time.sleep(3)
            
            # Проверяем авторизацию заново
            try:
                user_menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Меню пользователя')]")
                logger.info("✅ После очистки cookies - всё ещё авторизован")
            except:
                logger.error("❌ После очистки cookies потеряна авторизация!")
                raise Exception("Потеряна авторизация после очистки cookies")
        
        # Шаг 1: Нажать кнопку "Создать заявление" (если есть модалка) И затем "Начать"
        logger.info("🔍 Шаг 1: Ищу модалку с черновиком или кнопку 'Начать'...")
        time.sleep(1.5)  # Ждем загрузки страницы и модалки
        
        # Сначала пробуем найти модальное окно с "Создать заявление"
        try:
            modal_button = driver.find_element(By.XPATH, "//button[contains(., 'Создать заявление')]")
            driver.execute_script("arguments[0].click();", modal_button)
            logger.info("✅ Шаг 1a: Нажата кнопка 'Создать заявление' в модалке")
            time.sleep(1)  # Ждём закрытия модалки
        except:
            logger.info("   Модалка с 'Создать заявление' не найдена")
        
        # ВСЕГДА ищем и нажимаем кнопку "Начать" (независимо от модалки)
        try:
            start_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Начать')]"))
            )
            driver.execute_script("arguments[0].click();", start_button)
            logger.info("✅ Шаг 1b: Нажата кнопка 'Начать'")
            time.sleep(1)
        except Exception as e:
            logger.error(f"❌ Шаг 1: Кнопка 'Начать' не найдена: {e}")
            driver.save_screenshot("error_no_start_button.png")
            raise
        
        # Закрываем лишние окна после начала
        close_extra_windows(driver)
        
        # Шаг 2: "Предоставление земельного участка в аренду"
        logger.info("🔍 Шаг 2: Нажимаю 'Предоставление земельного участка в аренду'...")
        time.sleep(1)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Предоставление земельного участка в аренду')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)
        logger.info("✅ Шаг 2: Нажата")
        time.sleep(1)
        
        # Закрываем лишние окна
        close_extra_windows(driver)
        
        # Шаг 3: "Заявитель"
        logger.info("🔍 Шаг 3: Нажимаю 'Заявитель'...")
        time.sleep(1)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Заявитель')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)
        logger.info("✅ Шаг 3: Нажата")
        time.sleep(1)
        
        # Шаги 4-8: Нажать "Верно" 5 раз
        for i in range(4, 9):
            logger.info(f"🔍 Шаг {i}: Нажимаю 'Верно'...")
            time.sleep(1)
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Верно')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", button)
            logger.info(f"✅ Шаг {i}: Нажата")
            time.sleep(1)
        
        # Шаг 9: "Решение отсутствует"
        logger.info("🔍 Шаг 9: Нажимаю 'Решение отсутствует'...")
        time.sleep(1)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Решение отсутствует')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)
        logger.info("✅ Шаг 9: Нажата")
        time.sleep(1)
        
        # Шаг 10: Выбрать "Гражданин, испрашивающий участок для ИЖС и ЛПХ"
        logger.info("🔍 Шаг 10: Выбираю из выпадающего списка...")
        time.sleep(2)
        
        # Запоминаем текущее окно
        main_window = driver.current_window_handle
        
        # Закрыть возможные открытые меню
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)
        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(1)
        
        # Найти и кликнуть на dropdown
        js_dropdown = """
        var question = document.evaluate("//*[contains(text(), 'К какой категории относится заявитель')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (question) {
            var questionY = question.getBoundingClientRect().top;
            var dropdowns = document.querySelectorAll('div[role="button"], input[readonly]');
            for (var i = 0; i < dropdowns.length; i++) {
                var dd = dropdowns[i];
                var ddY = dd.getBoundingClientRect().top;
                if (ddY > questionY && dd.offsetWidth > 100 && dd.offsetHeight > 20) {
                    dd.scrollIntoView({block: 'center'});
                    dd.click();
                    return 'OK';
                }
            }
        }
        return 'ERROR';
        """
        
        result = driver.execute_script(js_dropdown)
        logger.info(f"   Результат клика на dropdown: {result}")
        time.sleep(1)
        
        # Выбрать опцию
        option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Гражданин, испрашивающий участок для ИЖС и ЛПХ')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", option)
        logger.info("✅ Шаг 10: Опция выбрана")
        time.sleep(1)
        
        # Проверяем и закрываем лишние окна
        close_extra_windows(driver)
        
        # Нажать "Далее"
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Далее')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", next_button)
        logger.info("✅ Шаг 10: Нажата кнопка 'Далее'")
        time.sleep(1)
        
        # Проверяем и закрываем лишние окна
        close_extra_windows(driver)
        
        # Шаг 11: Заполнить "Цель" и "Срок аренды"
        logger.info("🔍 Шаг 11: Заполняю поля 'Цель' и 'Срок аренды'...")
        time.sleep(2)
        
        js_fill_any = """
        var editables = [];
        
        var textareas = document.querySelectorAll('textarea');
        for (var i = 0; i < textareas.length; i++) {
            if (textareas[i].offsetWidth > 10 && textareas[i].offsetHeight > 10) {
                editables.push({type: 'textarea', elem: textareas[i]});
            }
        }
        
        var inputs = document.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            var inp = inputs[i];
            var type = inp.type || 'text';
            if (type !== 'password' && type !== 'hidden' && type !== 'checkbox' && type !== 'radio' && type !== 'submit' && type !== 'button') {
                if (inp.offsetWidth > 10 && inp.offsetHeight > 10) {
                    editables.push({type: 'input', elem: inp});
                }
            }
        }
        
        var contentEditables = document.querySelectorAll('[contenteditable="true"]');
        for (var i = 0; i < contentEditables.length; i++) {
            if (contentEditables[i].offsetWidth > 10 && contentEditables[i].offsetHeight > 10) {
                editables.push({type: 'contenteditable', elem: contentEditables[i]});
            }
        }
        
        var filled = [];
        
        // Первое поле = "20"
        if (editables.length > 0) {
            var e1 = editables[0];
            e1.elem.focus();
            if (e1.type === 'contenteditable') {
                e1.elem.textContent = '20';
            } else {
                e1.elem.value = '20';
            }
            var events = ['input', 'change', 'keyup', 'keydown', 'blur'];
            events.forEach(function(eventType) {
                var event = new Event(eventType, { bubbles: true, cancelable: true });
                e1.elem.dispatchEvent(event);
            });
            filled.push('Поле 1: "20"');
        }
        
        // Второе поле = "Для индивидуального жилищного строительства"
        if (editables.length > 1) {
            var e2 = editables[1];
            e2.elem.focus();
            if (e2.type === 'contenteditable') {
                e2.elem.textContent = 'Для индивидуального жилищного строительства';
            } else {
                e2.elem.value = 'Для индивидуального жилищного строительства';
            }
            var events = ['input', 'change', 'keyup', 'keydown', 'blur'];
            events.forEach(function(eventType) {
                var event = new Event(eventType, { bubbles: true, cancelable: true });
                e2.elem.dispatchEvent(event);
            });
            filled.push('Поле 2: "Для индивидуального жилищного строительства"');
        }
        
        return filled.length > 0 ? filled.join('; ') : 'ERROR';
        """
        
        result = driver.execute_script(js_fill_any)
        logger.info(f"   Результат: {result}")
        time.sleep(1)
        
        # Нажать "Далее"
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Далее')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", next_button)
        logger.info("✅ Шаг 11: Нажата кнопка 'Далее'")
        time.sleep(1)
        
        # Проверяем и закрываем лишние окна
        close_extra_windows(driver)
        
        # Шаг 12: Ввести кадастровый номер
        logger.info(f"🔍 Шаг 12: Ввожу кадастровый номер {cadastral_number}...")
        time.sleep(1)
        
        js_cadastral = f"""
        var editables = [];
        
        var textareas = document.querySelectorAll('textarea');
        for (var i = 0; i < textareas.length; i++) {{
            if (textareas[i].offsetWidth > 10 && textareas[i].offsetHeight > 10) {{
                editables.push({{type: 'textarea', elem: textareas[i]}});
            }}
        }}
        
        var inputs = document.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {{
            var inp = inputs[i];
            var type = inp.type || 'text';
            if (type !== 'password' && type !== 'hidden' && type !== 'checkbox' && type !== 'radio' && type !== 'submit' && type !== 'button') {{
                if (inp.offsetWidth > 10 && inp.offsetHeight > 10) {{
                    editables.push({{type: 'input', elem: inp}});
                }}
            }}
        }}
        
        if (editables.length > 0) {{
            var field = editables[0];
            field.elem.focus();
            field.elem.value = '{cadastral_number}';
            
            var events = ['input', 'change', 'keyup', 'keydown', 'blur'];
            events.forEach(function(eventType) {{
                var event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                field.elem.dispatchEvent(event);
            }});
            
            return 'OK';
        }}
        return 'ERROR';
        """
        
        result = driver.execute_script(js_cadastral)
        logger.info(f"   Результат: {result}")
        time.sleep(1)
        
        # ВАЖНО: После ввода кадастрового номера часто открывается новое окно!
        close_extra_windows(driver)
        
        # Нажать "Далее"
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Далее')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", next_button)
        logger.info("✅ Шаг 12: Нажата кнопка 'Далее'")
        time.sleep(1)
        
        # Проверяем и закрываем лишние окна
        close_extra_windows(driver)
        
        # Шаг 13: Выбрать уполномоченный орган
        logger.info(f"🔍 Шаг 13: Ищу уполномоченный орган для кадастрового номера '{cadastral_number}'...")
        
        # ВАЖНО: Проверяем, что мы на правильной странице формы
        current_url = driver.current_url
        if '/form' not in current_url and '/order/' not in current_url:
            logger.error(f"❌ Неправильная страница! URL: {current_url}")
            driver.save_screenshot(f"error_wrong_page_{cadastral_number.replace(':', '_')}.png")
            raise Exception("Скрипт попал не на страницу формы")
        
        # Увеличенная пауза для гарантированной загрузки страницы
        logger.info("   ⏳ Жду загрузки страницы (5 сек)...")
        time.sleep(5)
        
        # Дополнительная проверка: ждём появления формы и поля ввода
        logger.info("   🔍 Проверяю готовность страницы и поля ввода...")
        page_ready = False
        
        for check_attempt in range(5):
            try:
                # Проверяем, что страница полностью загружена
                ready_state = driver.execute_script("return document.readyState")
                
                # Проверяем наличие поля ввода
                has_input_field = driver.execute_script("""
                    var inputs = document.querySelectorAll('input[type="text"], input:not([type])');
                    var visibleInputs = 0;
                    for (var i = 0; i < inputs.length; i++) {
                        if (inputs[i].offsetWidth > 50 && inputs[i].offsetHeight > 10) {
                            visibleInputs++;
                        }
                    }
                    return visibleInputs > 0;
                """)
                
                if ready_state == 'complete' and has_input_field:
                    logger.info(f"   ✅ Страница и поле ввода готовы (попытка {check_attempt + 1})")
                    page_ready = True
                    break
                else:
                    logger.info(f"   ⏳ Ожидание... readyState={ready_state}, hasInput={has_input_field} (попытка {check_attempt + 1})")
                    time.sleep(2)
            except Exception as e:
                logger.warning(f"   ⚠️ Ошибка проверки (попытка {check_attempt + 1}): {e}")
                time.sleep(2)
        
        if not page_ready:
            logger.warning("   ⚠️ Не удалось убедиться в полной загрузке, продолжаю...")
        
        # Ещё одна небольшая пауза для надёжности
        time.sleep(1)
        
        # Получаем ПОЛНОЕ название ответственного органа из БД
        responsible_org = get_responsible_org_by_cadastral(cadastral_number)
        
        if not responsible_org:
            logger.error(f"❌ Шаг 13: Ответственный орган не найден в БД для кадастрового номера {cadastral_number}")
            driver.save_screenshot(f"error_no_org_in_db_{cadastral_number.replace(':', '_')}.png")
            raise Exception("Район не определен: ответственный орган не найден в БД")
        
        logger.info(f"   ✅ Из БД получен ответственный орган: '{responsible_org}'")
        
        # Сохраняем скриншот перед вводом
        driver.save_screenshot(f"debug_step13_before_{cadastral_number.replace(':', '_')}.png")
        logger.info(f"   📸 Скриншот сохранён: debug_step13_before_{cadastral_number.replace(':', '_')}.png")
        
        # Ищем поле ввода с расширенными критериями
        logger.info("   🔍 Ищу поле ввода уполномоченного органа...")
        
        # 1. Ждем появления хотя бы одного поля ввода (до 15 сек - увеличено для медленного интернета)
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        except:
            logger.warning("   ⚠️ Поля ввода не появились за 15 секунд")
        
        # 2. Скрипт поиска правильного поля (возвращает элемент)
        js_find_input = """
        var inputs = document.querySelectorAll('input');
        var targetInput = null;
        
        // Ищем ЛЮБОЕ видимое текстовое поле
        for (var i = 0; i < inputs.length; i++) {
            var inp = inputs[i];
            var type = inp.type || 'text';
            
            // Пропускаем явно не подходящие типы
            if (type === 'password' || type === 'hidden' || type === 'checkbox' || 
                type === 'radio' || type === 'submit' || type === 'button') {
                continue;
            }
            
            // Берём первое видимое поле с разумными размерами
            if (inp.offsetWidth > 50 && inp.offsetHeight > 10 && 
                !inp.disabled && !inp.readOnly) {
                targetInput = inp;
                break;
            }
        }
        return targetInput;
        """
        
        target_input = driver.execute_script(js_find_input)
        
        if not target_input:
             logger.error("❌ Шаг 13: Поле ввода уполномоченного органа не найдено")
             driver.save_screenshot(f"error_no_field_{cadastral_number.replace(':', '_')}.png")
             raise Exception("Поле ввода уполномоченного органа не найдено")
        
        logger.info(f"   ✅ Поле ввода найдено")
        
        # 3. Ввод текста с помощью ActionChains (эмуляция клавиатуры)
        try:
            # Прокручиваем к элементу
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_input)
            time.sleep(0.5)
            
            # Импорт ActionChains локально
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Кликаем (физический клик важен для фокуса)
            actions = ActionChains(driver)
            actions.move_to_element(target_input).click().perform()
            time.sleep(0.5)
            
            # Очищаем (через Keys) - более надежно чем .clear()
            target_input.send_keys(Keys.CONTROL + "a")
            target_input.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)
            
            # Вводим текст по буквам
            logger.info(f"   ⌨️ Ввожу название: '{responsible_org[:50]}...'")
            for char in responsible_org:
                target_input.send_keys(char)
                # Небольшая задержка для пробелов
                if char == ' ':
                    time.sleep(0.05)
            
            time.sleep(0.5)
            
            # Проверяем результат
            current_val = target_input.get_attribute('value')
            # Если пусто или слишком коротко, значит ввод не прошел
            if not current_val or len(current_val) < 3:
                logger.warning(f"   ⚠️ Ввод через send_keys не сработал (значение: '{current_val}'), пробую JS...")
                
                # Fallback: JS ввод
                escaped_org = responsible_org.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
                driver.execute_script(f"arguments[0].value = '{escaped_org}'; arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));", target_input)
            
        except Exception as e:
             logger.error(f"❌ Ошибка при вводе текста: {e}")
             # Пытаемся через JS как последний шанс
             escaped_org = responsible_org.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
             driver.execute_script(f"arguments[0].value = '{escaped_org}'; arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));", target_input)
        
        # Ждем появления результатов поиска (может быть список или карта)
        time.sleep(3)  # Вернул как было
        
        # Сохраняем скриншот после ввода
        driver.save_screenshot(f"debug_step13_after_{cadastral_number.replace(':', '_')}.png")
        logger.info(f"   📸 Скриншот после ввода: debug_step13_after_{cadastral_number.replace(':', '_')}.png")
        
        # Ищем и кликаем на найденную организацию (в списке слева или в выпадающем списке)
        logger.info(f"   🔍 Ищу организацию в результатах поиска...")
        
        time.sleep(1)  # Вернул как было
        
        clicked = False
        
        # Экранируем для поиска
        escaped_for_search = responsible_org.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        
        for attempt in range(5):
            logger.info(f"   Попытка {attempt + 1}/5...")
            
            # Ищем элемент, содержащий название организации
            js_click_org = f"""
            var searchTerm = '{escaped_for_search}';
            var cleanSearchTerm = searchTerm.replace(/\\s+/g, ' ').trim();
            
            // Ищем ВСЕ элементы на странице
            var allElements = document.querySelectorAll('*');
            
            var bestMatch = null;
            var bestMatchLength = 999999;
            
            for (var elem of allElements) {{
                var text = (elem.textContent || '').replace(/\\s+/g, ' ').trim();
                
                // Если элемент содержит название организации
                if (text.includes(cleanSearchTerm) && 
                    elem.offsetWidth > 50 && 
                    elem.offsetHeight > 20) {{
                    
                    // Берём элемент с самым коротким текстом (самый вложенный)
                    if (text.length < bestMatchLength && text.length < 300) {{
                        bestMatch = elem;
                        bestMatchLength = text.length;
                    }}
                }}
            }}
            
            if (bestMatch) {{
                bestMatch.scrollIntoView({{block: 'center'}});
                bestMatch.click();
                return {{success: true, text: bestMatch.textContent.substring(0, 150)}};
            }}
            
            return {{success: false}};
            """
            
            result = driver.execute_script(js_click_org)
            
            if result and result.get('success'):
                logger.info(f"   ✅ Кликнул на организацию!")
                logger.info(f"      Текст: {result.get('text', '')[:120]}")
                clicked = True
                break
            else:
                logger.warning(f"   ⚠️ Организация не найдена, жду еще...")
                time.sleep(1.5)  # Вернул как было
        
        if not clicked:
            logger.error(f"❌ Не удалось найти организацию '{responsible_org[:80]}'")
            driver.save_screenshot(f"error_no_org_{cadastral_number.replace(':', '_')}.png")
            raise Exception(f"Район не определен: организация не найдена")
        
        
        # Ждём появления кнопки "Выбрать" после выбора варианта
        time.sleep(1)  # Вернул как было
        logger.info("   Ищу кнопку 'Выбрать'...")
        
        # Пытаемся найти кнопку "Выбрать" до 10 попыток (может быть уже на странице)
        select_clicked = False
        for attempt in range(10):
            js_click_select = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var btn = buttons[i];
                var text = btn.textContent || '';
                // Ищем кнопку со словом "Выбрать"
                if (text.trim().startsWith('Выбрать') && btn.offsetWidth > 50 && btn.offsetHeight > 20) {
                    btn.scrollIntoView({block: 'center'});
                    btn.click();
                    return 'OK: Clicked [' + text.trim() + ']';
                }
            }
            return 'ERROR: Button not found';
            """
            
            result = driver.execute_script(js_click_select)
            
            if 'OK' in result:
                logger.info(f"   ✅ {result}")
                select_clicked = True
                break
            else:
                if attempt < 9:
                    if attempt % 2 == 0:  # Логируем каждую 2-ю попытку
                        logger.info(f"   Попытка {attempt + 1}/10: кнопка не найдена, жду еще...")
                    time.sleep(0.8)  # Вернул как было
        
        if not select_clicked:
            logger.warning("⚠️ Кнопка 'Выбрать' не найдена, пробую продолжить без неё...")
            # НЕ бросаем ошибку - может кнопка не нужна, пробуем продолжить
        
        logger.info("✅ Шаг 13: Нажата кнопка 'Выбрать'")
        time.sleep(1.5)  # Вернул как было
        
        # Проверяем и закрываем лишние окна (может открыться карта)
        close_extra_windows(driver)
        
        # Шаг 14: "Электронно в личном кабинете"
        logger.info("🔍 Шаг 14: Нажимаю 'Электронно в личном кабинете'...")
        time.sleep(1)
        
        # Ищем кнопку с этим текстом
        try:
            # Пробуем найти через XPath
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Электронно в личном кабинете')] | //*[contains(text(), 'Электронно в личном кабинете')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", button)
            logger.info("   ✅ Кнопка нажата через XPath")
        except:
            # Если XPath не сработал - пробуем JavaScript
            js_click = """
            var buttons = document.querySelectorAll('button, div, span, a');
            for (var btn of buttons) {
                var text = (btn.textContent || '').trim();
                if (text.includes('Электронно в личном кабинете') && btn.offsetWidth > 10 && btn.offsetHeight > 10) {
                    btn.scrollIntoView({block: 'center'});
                    btn.click();
                    return 'OK';
                }
            }
            return 'ERROR';
            """
            result = driver.execute_script(js_click)
            if result == 'OK':
                logger.info("   ✅ Кнопка нажата через JavaScript")
            else:
                logger.warning("   ⚠️ Кнопка не найдена, пробую продолжить...")
        
        time.sleep(1)
        
        # Шаг 15: "Отправить заявление"
        logger.info("🔍 Шаг 15: Нажимаю 'Отправить заявление'...")
        time.sleep(1)
        
        # Ищем кнопку - точно так же, как кнопку "Далее"
        try:
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Отправить заявление')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", submit_button)
            logger.info("✅ Шаг 15: Нажата кнопка 'Отправить заявление'")
        except Exception as e:
            logger.error(f"❌ Не удалось нажать 'Отправить заявление': {e}")
            driver.save_screenshot(f"error_submit_button_{cadastral_number.replace(':', '_')}.png")
        
        time.sleep(1.5)
        
        # Проверяем, что заявка создана (URL должен содержать /order/ или должен быть текст подтверждения)
        logger.info("🔍 Проверяю создание заявки...")
        current_url = driver.current_url
        
        # Проверка 1: URL содержит /order/
        if '/order/' in current_url:
            logger.info(f"   ✅ Заявка создана! URL: {current_url}")
        else:
            # Проверка 2: На странице есть текст подтверждения
            try:
                success_texts = ['заявлен', 'создан', 'принят', 'отправлен']
                page_text = driver.page_source.lower()
                
                if any(text in page_text for text in success_texts):
                    logger.info(f"   ✅ Заявка создана! (найден текст подтверждения)")
                    
                    # === ИЗВЛЕКАЕМ НОМЕР ЗАЯВЛЕНИЯ ===
                    try:
                        logger.info("   🔍 Ищу номер заявления...")
                        time.sleep(2)  # Даём время на отображение номера
                        
                        # Возможные варианты текста с номером заявления:
                        # "Номер заявления: 123456789"
                        # "Заявление № 123456789"
                        # "№ заявления: 123456789"
                        
                        # Ищем элементы, содержащие номер
                        number_patterns = [
                            "//div[contains(., 'Номер заявления') or contains(., 'номер заявления')]",
                            "//p[contains(., 'Номер заявления') or contains(., 'номер заявления')]",
                            "//span[contains(., 'Номер заявления') or contains(., 'номер заявления')]",
                            "//div[contains(., 'Заявление №') or contains(., 'заявление №')]",
                            "//p[contains(., 'Заявление №') or contains(., 'заявление №')]",
                        ]
                        
                        application_number = None
                        for pattern in number_patterns:
                            try:
                                elements = driver.find_elements(By.XPATH, pattern)
                                for element in elements:
                                    text = element.text.strip()
                                    # Извлекаем числа из текста
                                    import re
                                    numbers = re.findall(r'\d{6,}', text)  # Ищем числа из 6+ цифр
                                    if numbers:
                                        application_number = numbers[0]
                                        logger.info(f"   📋 Найден номер заявления: {application_number}")
                                        break
                                if application_number:
                                    break
                            except:
                                continue
                        
                        if not application_number:
                            # Альтернативный способ: поиск в тексте страницы
                            import re
                            full_text = driver.find_element(By.TAG_NAME, 'body').text
                            # Ищем паттерны типа "№ 123456789" или "номер 123456789"
                            matches = re.findall(r'(?:номер|№)\s*:?\s*(\d{6,})', full_text, re.IGNORECASE)
                            if matches:
                                application_number = matches[0]
                                logger.info(f"   📋 Найден номер заявления (альтернативный поиск): {application_number}")
                        
                        if application_number:
                            # Сохраняем скриншот с номером для подтверждения
                            driver.save_screenshot(f"success_app_{application_number}_{cadastral_number.replace(':', '_')}.png")
                            logger.info(f"   📸 Скриншот с номером заявления сохранён")
                            return application_number  # Возвращаем номер
                        else:
                            logger.warning("   ⚠️ Номер заявления не найден на странице")
                            driver.save_screenshot(f"success_no_number_{cadastral_number.replace(':', '_')}.png")
                            return None
                    
                    except Exception as e:
                        logger.warning(f"   ⚠️ Ошибка при извлечении номера заявления: {e}")
                        return None
                else:
                    logger.warning(f"   ⚠️ Не уверен, что заявка создана. URL: {current_url}")
                    driver.save_screenshot(f"unclear_status_{cadastral_number.replace(':', '_')}.png")
                    return None
            except:
                logger.warning("   ⚠️ Не могу проверить статус заявки")
                return None
        
        logger.info(f"✅ Заявка для {cadastral_number} отправлена!")
        return True  # Для обратной совместимости, если номер не нужен
        
    except Exception as e:
        logger.error(f"❌ Ошибка при заполнении формы для {cadastral_number}: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"error_{cadastral_number.replace(':', '_')}.png")
        return False

def setup_browser(headless=False):
    """
    Настройка и запуск браузера Chrome
    
    Args:
        headless: Запустить в headless режиме (без GUI)
    """
    logger.info("🔧 Настройка браузера...")
    
    if headless:
        logger.info("   🔇 Режим: headless (фоновый, без GUI)")
    else:
        logger.info("   🖥️  Режим: обычный (с GUI)")
    
    profile_dir = os.path.abspath("./selenium_chrome_profile")
    
    chrome_options = Options()
    
    # Headless режим
    if headless:
        chrome_options.add_argument("--headless=new")  # Новый headless режим Chrome
        chrome_options.add_argument("--window-size=1920,1080")  # Размер окна для headless
        chrome_options.add_argument("--disable-gpu")  # Отключение GPU в headless
        chrome_options.add_argument("--no-sandbox")  # Для стабильности в headless
        chrome_options.add_argument("--disable-dev-shm-usage")  # Преодоление ограничений ресурсов
        chrome_options.add_argument("--disable-software-rasterizer")  # Отключение программной растеризации
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    else:
        chrome_options.add_argument("--start-maximized")
    
    # Общие настройки
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Обход SSL предупреждений
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    
    # ВАЖНО: Блокируем popup окна и новые вкладки
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.popups": 2,  # Блокировать popups
        "profile.popup_exceptions": {},
    })
    
    # chrome_options.add_argument(f"--user-data-dir={profile_dir}")  # Временно отключено из-за конфликта
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def close_extra_windows(driver):
    """Закрыть все лишние окна, оставить только первое"""
    try:
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            logger.warning(f"⚠️ Обнаружено {len(all_windows)} окон! Закрываю лишние...")
            first_window = all_windows[0]
            for i, window in enumerate(all_windows):
                if i > 0:  # Закрываем все кроме первого
                    try:
                        driver.switch_to.window(window)
                        logger.info(f"   Закрыто окно {i+1}")
                        driver.close()
                    except Exception as e:
                        logger.warning(f"   Не удалось закрыть окно {i+1}: {e}")
            driver.switch_to.window(first_window)
            logger.info("✅ Переключен обратно на основное окно")
            time.sleep(1)
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при закрытии лишних окон: {e}")
        return False

def main():
    """Главная функция"""
    logger.info("="*80)
    logger.info("🚀 АВТОМАТИЧЕСКАЯ ОТПРАВКА ЗАЯВЛЕНИЙ НА АРЕНДУ ЗЕМЛИ")
    logger.info("="*80)
    
    # === АВТОМАТИЧЕСКАЯ МИГРАЦИЯ БД ===
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Пытаемся добавить колонку cadastral_cost, если её нет
            cursor.execute("ALTER TABLE land_records ADD COLUMN cadastral_cost REAL")
            conn.commit()
            logger.info("✅ Колонка 'cadastral_cost' успешно добавлена в БД")
        except sqlite3.OperationalError:
            # Колонка уже существует - это нормально
            pass
        conn.close()
    except Exception as e:
        logger.warning(f"⚠️ Ошибка при проверке структуры БД: {e}")
    
    # Запрашиваем у пользователя регионы
    selected_regions = ask_for_regions()
    
    if selected_regions is not None and len(selected_regions) == 0:
        logger.info("❌ Регионы не выбраны. Выход.")
        return
    
    # Запрашиваем диапазон кадастровой стоимости
    print("\n" + "-"*80)
    print("💰 ФИЛЬТР ПО КАДАСТРОВОЙ СТОИМОСТИ")
    print("-" * 80)
    
    cost_min_str = input("👉 Введите минимальную стоимость (от, Enter = 0): ").strip()
    cost_max_str = input("👉 Введите максимальную стоимость (до, Enter = без ограничений): ").strip()
    
    try:
        cost_min = float(cost_min_str) if cost_min_str else 0
    except ValueError:
        cost_min = 0
        print("⚠️ Некорректное значение min, использую 0")
        
    try:
        cost_max = float(cost_max_str) if cost_max_str else float('inf')
    except ValueError:
        cost_max = float('inf')
        print("⚠️ Некорректное значение max, использую бесконечность")
    
    print(f"✅ Фильтр установлен: от {cost_min} до {'∞' if cost_max == float('inf') else cost_max}")
    
    # Всегда запускаем в обычном режиме (с GUI)
    headless_mode = False
    
    # Получить список участков для отправки
    parcels = get_parcels_to_submit(region_codes=selected_regions)
    logger.info(f"📊 Найдено участков для отправки: {len(parcels)}")
    
    if not parcels:
        logger.info("✅ Все заявления уже отправлены!")
        return
    
    # Подсчет по районам
    districts_count = {}
    for parcel in parcels:
        district = parcel[3]  # district name
        district_code = parcel[4]  # district_code
        district_label = f"{district} ({district_code})"
        districts_count[district_label] = districts_count.get(district_label, 0) + 1
    
    logger.info(f"📊 Районов: {len(districts_count)}")
    for district, count in sorted(districts_count.items()):
        logger.info(f"   {district}: {count} участков")
    
    # Настройка браузера
    driver = setup_browser(headless=headless_mode)
    wait = WebDriverWait(driver, 45)  # Увеличен таймаут до 45 секунд для headless
    
    try:
        # Проверка авторизации
        logger.info("\n🔐 Проверка авторизации...")
        driver.get("https://www.gosuslugi.ru")
        time.sleep(3)  # Даём больше времени на загрузку в headless
        
        try:
            user_menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Меню пользователя')]")
            logger.info("✅ Пользователь авторизован")
        except:
            logger.warning("⚠️ Пользователь не авторизован, пытаюсь войти...")
            
            try:
                # Ждём полной загрузки страницы
                logger.info("   ⏳ Жду загрузки главной страницы...")
                time.sleep(3)
                
                # Сохраняем скриншот для отладки
                if headless_mode:
                    try:
                        driver.save_screenshot("headless_debug_main_page.png")
                        logger.info("   📸 Скриншот главной страницы: headless_debug_main_page.png")
                    except:
                        pass
                
                # Ищем кнопку "Войти" с несколькими попытками
                logger.info("   🔍 Ищу кнопку 'Войти'...")
                login_button = None
                for attempt in range(3):
                    try:
                        login_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти')]"))
                        )
                        break
                    except:
                        logger.info(f"   ⏳ Попытка {attempt + 1}/3...")
                        time.sleep(2)
                
                if not login_button:
                    raise Exception("Кнопка 'Войти' не найдена после 3 попыток")
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", login_button)
                logger.info("   ✅ Нажата кнопка 'Войти'")
                time.sleep(5)  # Увеличил время ожидания загрузки формы
                
                # Ждем появления поля логина
                try:
                    logger.info("   🔍 Ищу форму логина...")
                    
                    # Скриншот формы логина для отладки
                    if headless_mode:
                        try:
                            driver.save_screenshot("headless_debug_login_form.png")
                            logger.info("   📸 Скриншот формы логина: headless_debug_login_form.png")
                        except:
                            pass
                    
                    login_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@name='login' or @type='tel' or @id='login']"))
                    )
                    logger.info("   ✅ Форма логина найдена")
                    current_login = login_field.get_attribute('value') or ''
                    
                    if '+79295154970' in current_login:
                        logger.info("✅ Логин уже подставлен, ввожу только пароль")
                        # Ищем поле пароля
                        password_field = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@name='password' or @type='password']"))
                        )
                        password_field.clear()
                        password_field.send_keys("_4_BW:%rcn6")
                        logger.info("   Пароль введен")
                        time.sleep(2)
                        
                        # Нажимаем кнопку входа
                        try:
                            submit_button = wait.until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти') and not(contains(text(), 'удаётся'))]"))
                            )
                            # Прокручиваем к кнопке
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                            time.sleep(0.5)
                            # Обычный клик
                            submit_button.click()
                            logger.info("   ✅ Кнопка входа нажата")
                            time.sleep(2)
                        except Exception as e:
                            logger.warning(f"   ⚠️ Не удалось нажать кнопку входа автоматически: {e}")
                            logger.info("   👉 НАЖМИТЕ КНОПКУ 'ВОЙТИ' ВРУЧНУЮ")
                        
                    else:
                        logger.info("📝 Ввожу логин и пароль")
                        # Вводим логин
                        login_field.clear()
                        login_field.send_keys("+79295154970")
                        logger.info("   Логин введен")
                        time.sleep(2)
                        
                        # Ищем и вводим пароль
                        password_field = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@name='password' or @type='password']"))
                        )
                        password_field.clear()
                        password_field.send_keys("_4_BW:%rcn6")
                        logger.info("   Пароль введен")
                        time.sleep(2)
                        
                        # Нажимаем кнопку входа
                        try:
                            submit_button = wait.until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти') and not(contains(text(), 'удаётся'))]"))
                            )
                            # Прокручиваем к кнопке
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                            time.sleep(0.5)
                            # Обычный клик
                            submit_button.click()
                            logger.info("   ✅ Кнопка входа нажата")
                            time.sleep(2)
                        except Exception as e:
                            logger.warning(f"   ⚠️ Не удалось нажать кнопку входа автоматически: {e}")
                            logger.info("   👉 НАЖМИТЕ КНОПКУ 'ВОЙТИ' ВРУЧНУЮ")
                    
                    # Ждем SMS код
                    if headless_mode:
                        # В headless режиме вводим SMS через терминал
                        logger.info("📱 Ожидаю ввода SMS-кода...")
                        logger.info("   SMS-код будет отправлен на номер +79295154970")
                        
                        # Даём время на получение SMS
                        time.sleep(5)
                        
                        # Запрашиваем код у пользователя
                        sms_code = input("\n👉 Введите SMS-код: ").strip()
                        
                        if sms_code:
                            logger.info(f"   Получен код: {sms_code}")
                            
                            # Ищем поле для SMS и вводим код
                            try:
                                sms_field = wait.until(
                                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @inputmode='numeric' or contains(@placeholder, 'код')]"))
                                )
                                sms_field.clear()
                                sms_field.send_keys(sms_code)
                                logger.info("   ✅ SMS-код введён")
                                time.sleep(1)
                                
                                # Нажимаем кнопку "Войти" или "Подтвердить"
                                try:
                                    confirm_button = wait.until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти') or contains(., 'Подтвердить')]"))
                                    )
                                    driver.execute_script("arguments[0].click();", confirm_button)
                                    logger.info("   ✅ Кнопка подтверждения нажата")
                                    time.sleep(3)
                                except:
                                    logger.warning("   ⚠️ Кнопка подтверждения не найдена, код может быть введён автоматически")
                                
                            except Exception as e:
                                logger.error(f"   ❌ Ошибка при вводе SMS-кода: {e}")
                        
                        # Проверяем авторизацию
                        for i in range(30):
                            try:
                                user_menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Меню пользователя')]")
                                logger.info("✅ Авторизация успешна!")
                                break
                            except:
                                if i % 10 == 0 and i > 0:
                                    logger.info(f"   ⏳ Проверка авторизации... ({i} сек)")
                                time.sleep(1)
                        else:
                            logger.error("❌ Не удалось авторизоваться после ввода SMS-кода")
                        
                        # === ВЫБОР ПРОФИЛЯ ПОСЛЕ АВТОРИЗАЦИИ (HEADLESS) ===
                        logger.info("\n🔍 Проверка необходимости выбора профиля...")
                        time.sleep(2)
                        
                        try:
                            # Проверяем, есть ли кнопка "Пропустить"
                            skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Пропустить') or contains(text(), 'пропустить')]")
                            logger.info("   ⚙️  Найдена кнопка 'Пропустить'")
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skip_button)
                            time.sleep(0.5)
                            skip_button.click()
                            logger.info("   ✅ Нажата кнопка 'Пропустить'")
                            time.sleep(2)
                        except:
                            logger.info("   ℹ️  Кнопка 'Пропустить' не найдена (это нормально)")
                        
                        try:
                            # Проверяем, нужно ли выбрать профиль
                            profile_button = driver.find_element(By.XPATH, "//button[contains(., 'Абрамян') or contains(., 'частное лицо') or contains(., 'Частное лицо')]")
                            logger.info("   👤 Найдена кнопка выбора профиля (Абрамян П. Р. / Частное лицо)")
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_button)
                            time.sleep(0.5)
                            profile_button.click()
                            logger.info("   ✅ Выбран профиль 'Частное лицо'")
                            time.sleep(2)
                        except:
                            logger.info("   ℹ️  Выбор профиля не требуется (уже выбран)")
                        
                        logger.info("✅ Настройка профиля завершена\n")
                    else:
                        # В обычном режиме - ручной ввод в браузере
                        logger.info("⏳ Ожидаю ввода SMS-кода (480 секунд)...")
                        logger.info("   👉 ВВЕДИТЕ SMS-КОД В БРАУЗЕРЕ И НАЖМИТЕ ВОЙТИ ВРУЧНУЮ")
                        
                        for i in range(480):
                            try:
                                user_menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Меню пользователя')]")
                                logger.info("✅ Авторизация успешна!")
                                break
                            except:
                                if i % 20 == 0 and i > 0:
                                    logger.info(f"   ⏳ Осталось {480 - i} секунд...")
                                time.sleep(1)
                        
                        # === ВЫБОР ПРОФИЛЯ ПОСЛЕ АВТОРИЗАЦИИ (ОБЫЧНЫЙ РЕЖИМ) ===
                        logger.info("\n🔍 Проверка необходимости выбора профиля...")
                        time.sleep(2)
                        
                        try:
                            # Проверяем, есть ли кнопка "Пропустить" (предложение добавить данные)
                            skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Пропустить') or contains(text(), 'пропустить')]")
                            logger.info("   ⚙️  Найдена кнопка 'Пропустить'")
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skip_button)
                            time.sleep(0.5)
                            skip_button.click()
                            logger.info("   ✅ Нажата кнопка 'Пропустить'")
                            time.sleep(2)
                        except:
                            logger.info("   ℹ️  Кнопка 'Пропустить' не найдена (это нормально)")
                        
                        try:
                            # Проверяем, нужно ли выбрать профиль (Частное лицо / Организация)
                            profile_button = driver.find_element(By.XPATH, "//button[contains(., 'Абрамян') or contains(., 'частное лицо') or contains(., 'Частное лицо')]")
                            logger.info("   👤 Найдена кнопка выбора профиля (Абрамян П. Р. / Частное лицо)")
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_button)
                            time.sleep(0.5)
                            profile_button.click()
                            logger.info("   ✅ Выбран профиль 'Частное лицо'")
                            time.sleep(2)
                        except:
                            logger.info("   ℹ️  Выбор профиля не требуется (уже выбран)")
                    
                    logger.info("✅ Настройка профиля завершена\n")
                except Exception as e:
                    logger.error(f"❌ Ошибка при вводе логина/пароля: {e}")
                    logger.info("⏳ Ожидаю 240 секунд для ручного входа...")
                    time.sleep(240)
                    
            except Exception as e:
                logger.error(f"❌ Ошибка при входе: {e}")
                logger.info("⏳ Ожидаю 120 секунд для ручного входа...")
                time.sleep(120)
        
        # === НОВЫЙ ШАГ: ПЕРЕХОД НА РОСРЕЕСТР ===
        logger.info("\n" + "="*80)
        logger.info("🏛️  ПЕРЕХОД НА СТРАНИЦУ РОСРЕЕСТРА")
        logger.info("="*80)
        
        try:
            rosreestr_url = "https://lk.rosreestr.ru/eservices/real-estate-objects-online"
            logger.info(f"📍 Переход на: {rosreestr_url}")
            driver.get(rosreestr_url)
            
            logger.info("⏳ Ожидание загрузки страницы (3 секунды)...")
            time.sleep(3)
            
            # === ОБХОД ПРЕДУПРЕЖДЕНИЯ О БЕЗОПАСНОСТИ (если появится) ===
            try:
                logger.info("🔍 Проверка предупреждения SSL...")
                
                # Проверяем, есть ли кнопка "Дополнительные настройки" или "Advanced"
                advanced_button = None
                try:
                    advanced_button = driver.find_element(By.ID, "details-button")
                except:
                    try:
                        advanced_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Дополнительные') or contains(text(), 'Advanced')]")
                    except:
                        pass
                
                if advanced_button:
                    logger.info("   ⚠️  Обнаружено предупреждение SSL")
                    logger.info("   🔧 Клик на 'Дополнительные настройки'...")
                    advanced_button.click()
                    time.sleep(1)
                    
                    # Ищем кнопку "Перейти на сайт (небезопасно)"
                    proceed_button = None
                    try:
                        proceed_button = driver.find_element(By.ID, "proceed-link")
                    except:
                        try:
                            proceed_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Перейти') or contains(text(), 'Proceed')]")
                        except:
                            pass
                    
                    if proceed_button:
                        logger.info("   🔧 Клик на 'Перейти на сайт lk.rosreestr.ru (небезопасно)'...")
                        proceed_button.click()
                        time.sleep(2)
                        logger.info("   ✅ Предупреждение обойдено!")
                    else:
                        logger.warning("   ⚠️  Кнопка 'Перейти' не найдена, но это может быть нормально")
                else:
                    logger.info("   ✅ Предупреждение SSL не обнаружено (сайт в исключениях или сертификат действителен)")
            except Exception as e:
                logger.warning(f"   ⚠️  Не удалось обойти предупреждение SSL: {e}")
                logger.info("   ℹ️  Продолжаем работу...")
            
            # === ВХОД НА РОСРЕЕСТР ЧЕРЕЗ ГОСУСЛУГИ ===
            logger.info("\n🔑 Авторизация на Росреестре...")
            
            # Сначала делаем скриншот для отладки
            logger.info("   📸 Сохранение скриншота страницы для поиска кнопки 'Войти'...")
            driver.save_screenshot(f"rosreestr_before_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            time.sleep(2)
            
            try:
                # Ищем кнопку "Войти" (может быть разных форматов)
                login_button = None
                
                # Попытка 1: Кнопка в правом верхнем углу (обычное расположение)
                logger.info("   🔍 Попытка 1: Ищем кнопку в header/nav...")
                try:
                    login_button = driver.find_element(By.XPATH, "//header//button[contains(text(), 'Войти')] | //nav//button[contains(text(), 'Войти')]")
                    logger.info("   ✅ Найдена кнопка 'Войти' в header/nav")
                except:
                    pass
                
                # Попытка 2: Любая кнопка с текстом "Войти"
                if not login_button:
                    logger.info("   🔍 Попытка 2: Ищем любую кнопку с текстом 'Войти'...")
                    try:
                        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
                        logger.info("   ✅ Найдена кнопка 'Войти' (текст)")
                    except:
                        pass
                
                # Попытка 3: Ссылка с текстом "Войти"
                if not login_button:
                    logger.info("   🔍 Попытка 3: Ищем ссылку с текстом 'Войти'...")
                    try:
                        login_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Войти')]")
                        logger.info("   ✅ Найдена ссылка 'Войти'")
                    except:
                        pass
                
                # Попытка 4: Элемент с aria-label или title
                if not login_button:
                    logger.info("   🔍 Попытка 4: Ищем по aria-label/title...")
                    try:
                        login_button = driver.find_element(By.XPATH, "//*[@aria-label='Войти'] | //*[@title='Войти']")
                        logger.info("   ✅ Найден элемент с aria-label/title 'Войти'")
                    except:
                        pass
                
                # Попытка 5: Любой кликабельный элемент, содержащий слово "войти" (регистронезависимо)
                if not login_button:
                    logger.info("   🔍 Попытка 5: Ищем любой элемент со словом 'войти'...")
                    try:
                        all_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ВОЙТИ', 'войти'), 'войти')]")
                        for elem in all_elements:
                            if elem.is_displayed() and elem.is_enabled():
                                login_button = elem
                                logger.info(f"   ✅ Найден элемент: {elem.tag_name} с текстом '{elem.text[:50]}'")
                                break
                    except:
                        pass
                
                if login_button:
                    logger.info("   🔧 Клик на кнопку 'Войти'...")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", login_button)
                    
                    logger.info("   ⏳ Ожидание перенаправления на Госуслуги (20 секунд)...")
                    time.sleep(20)
                    
                    logger.info("   ✅ Вход выполнен!")
                    logger.info(f"   📍 Текущий URL: {driver.current_url}")
                else:
                    logger.warning("   ⚠️  Кнопка 'Войти' не найдена после 5 попыток!")
                    screenshot_name = f"rosreestr_login_not_found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    driver.save_screenshot(screenshot_name)
                    logger.warning(f"   📸 Скриншот сохранён: {screenshot_name}")
                    
                    # Проверяем, может уже залогинены - ищем признаки авторизации
                    logger.info("   🔍 Проверяю, может уже авторизован...")
                    page_text = driver.execute_script("return document.body.innerText;")
                    if any(keyword in page_text.lower() for keyword in ['выход', 'профиль', 'личный кабинет', 'абрамян']):
                        logger.info("   ✅ Похоже, уже авторизован (найдены ключевые слова)")
                    else:
                        logger.error("   ❌ НЕ авторизован и кнопка 'Войти' не найдена!")
                        logger.info("   📍 Текущий URL: " + driver.current_url)
                    logger.warning("   📸 Проверьте скриншот: rosreestr_before_login_*.png")
                    logger.info("   ℹ️  Возможно, уже авторизованы или страница изменилась")
            
            except Exception as e:
                logger.warning(f"   ⚠️  Ошибка при входе: {e}")
                logger.info("   ℹ️  Возможно, уже авторизованы. Продолжаем...")
                import traceback
                traceback.print_exc()
            
            # === ФИНАЛЬНЫЙ ПЕРЕХОД НА СТРАНИЦУ ПОИСКА ===
            logger.info("\n📍 Финальный переход на страницу поиска объектов...")
            driver.get(rosreestr_url)
            time.sleep(3)
            
            logger.info("📸 Сохранение скриншота страницы Росреестра...")
            driver.save_screenshot(f"rosreestr_ready_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            logger.info("✅ Росреестр готов к работе!")
            logger.info(f"📍 Текущий URL: {driver.current_url}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при переходе на Росреестр: {e}")
            import traceback
            traceback.print_exc()
        
        # ======================================================================
        # ЦИКЛ ОБРАБОТКИ УЧАСТКОВ: ПРОВЕРКА + ОТПРАВКА
        # ======================================================================
        logger.info("\n" + "="*80)
        logger.info("🔄 НАЧАЛО ЦИКЛА ОБРАБОТКИ УЧАСТКОВ")
        logger.info("="*80)
        
        success_count = 0
        error_count = 0
        occupied_count = 0
        not_found_count = 0
        
        for idx, (parcel_id, cadastral, address, district, district_code) in enumerate(parcels, 1):
            logger.info("\n" + "="*80)
            logger.info(f"📝 Участок {idx}/{len(parcels)}")
            logger.info(f"   ID: {parcel_id}")
            logger.info(f"   Кадастровый номер: {cadastral}")
            logger.info(f"   Район: {district} (код: {district_code})")
            logger.info(f"   Адрес: {(address or 'Не указан')[:100]}...")
            logger.info("="*80)
            
            try:
                # 0. ПРОВЕРКА СТОИМОСТИ (ЕСЛИ ЕСТЬ В БД)
                try:
                    conn = get_db_connection()
                    row = conn.execute("SELECT cadastral_cost FROM land_records WHERE id = ?", (parcel_id,)).fetchone()
                    conn.close()
                    
                    if row and row[0] is not None:
                        current_cost = row[0]
                        if not (cost_min <= current_cost <= cost_max):
                            logger.warning(f"⚠️ Участок {cadastral} пропущен по стоимости (из БД): {current_cost} (вне диапазона {cost_min}-{cost_max})")
                            # Пауза перед следующим
                            if idx < len(parcels):
                                time.sleep(1)
                            continue
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка проверки стоимости в БД: {e}")

                # ===================================================================
                # ЭТАП 1: ПРОВЕРКА ОБРЕМЕНЕНИЙ НА РОСРЕЕСТРЕ
                # ===================================================================
                logger.info("\n🏛️  ЭТАП 1: ПРОВЕРКА НА РОСРЕЕСТРЕ")
                check_success, encumbrances = check_encumbrances_rosreestr(driver, wait, cadastral)
                
                if not check_success:
                    # Не удалось выполнить проверку (скорее всего, кадастр не найден)
                    logger.error(f"❌ Участок {idx}/{len(parcels)}: Не найден на Росреестре")
                    update_parcel_status(parcel_id, "Не найден на Росреестре", error_message="Кадастр не найден в системе Росреестра")
                    not_found_count += 1
                    
                    # Пауза перед следующим участком
                    if idx < len(parcels):
                        logger.info("⏳ Пауза 3 секунды перед следующим участком...")
                        time.sleep(3)
                    continue
                
                # Проверка успешна, анализируем обременения
                if encumbrances:
                    # ЕСТЬ ОБРЕМЕНЕНИЯ - пропускаем участок
                    logger.warning(f"⚠️  Участок {idx}/{len(parcels)}: ОБНАРУЖЕНЫ ОБРЕМЕНЕНИЯ")
                    logger.info(f"   📋 Обременения: {encumbrances[:200]}...")
                    update_parcel_status(parcel_id, "Занят", encumbrances=encumbrances)
                    occupied_count += 1
                    
                    # Пауза перед следующим участком
                    if idx < len(parcels):
                        logger.info("⏳ Пауза 3 секунды перед следующим участком...")
                        time.sleep(3)
                    continue
                
                # НЕТ ОБРЕМЕНЕНИЙ - можно отправлять заявление
                logger.info("✅ Обременений НЕТ - можно отправлять заявление!")
                
                # 1.5 ПРОВЕРКА СТОИМОСТИ ПОСЛЕ РОСРЕЕСТРА (ОНА МОГЛА ПОЯВИТЬСЯ)
                try:
                    conn = get_db_connection()
                    row = conn.execute("SELECT cadastral_cost FROM land_records WHERE id = ?", (parcel_id,)).fetchone()
                    conn.close()
                    
                    if row and row[0] is not None:
                        current_cost = row[0]
                        if not (cost_min <= current_cost <= cost_max):
                            logger.warning(f"⚠️ Участок {cadastral} пропущен по стоимости (после проверки): {current_cost} (вне диапазона {cost_min}-{cost_max})")
                            # Пауза перед следующим
                            if idx < len(parcels):
                                logger.info("⏳ Пауза 3 секунды...")
                                time.sleep(3)
                            continue
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка повторной проверки стоимости: {e}")
                
                # ===================================================================
                # ЭТАП 2: ОТПРАВКА ЗАЯВЛЕНИЯ НА ГОСУСЛУГАХ
                # ===================================================================
                logger.info("\n📝 ЭТАП 2: ОТПРАВКА ЗАЯВЛЕНИЯ НА ГОСУСЛУГАХ")
                
                # Проверяем наличие ответственного органа в БД
                responsible_org = get_responsible_org_by_cadastral(cadastral)
                if responsible_org:
                    logger.info(f"   📋 Ответственный орган: {responsible_org[:120]}{'...' if len(responsible_org) > 120 else ''}")
                else:
                    logger.warning(f"   ⚠️ Ответственный орган НЕ НАЙДЕН в БД!")
                
                result = fill_form(driver, wait, cadastral)
                
                if result:
                    # result может быть True (старый формат) или номер заявления (строка)
                    if isinstance(result, str):
                        # Получен номер заявления
                        application_number = result
                        update_parcel_status(parcel_id, "Отправлено", application_number=application_number)
                        success_count += 1
                        logger.info(f"✅ Заявка {idx}/{len(parcels)} отправлена успешно! Номер: {application_number}")
                    else:
                        # Старый формат - просто True
                        update_parcel_status(parcel_id, "Отправлено")
                        success_count += 1
                        logger.info(f"✅ Заявка {idx}/{len(parcels)} отправлена успешно!")
                else:
                    update_parcel_status(parcel_id, "Ошибка", "Не удалось заполнить форму")
                    error_count += 1
                    logger.error(f"❌ Ошибка при отправке заявки {idx}/{len(parcels)}")
                
                # Пауза между заявками
                if idx < len(parcels):
                    logger.info("⏳ Пауза 5 секунд перед следующей заявкой...")
                    time.sleep(5)
                    
            except Exception as e:
                error_str = str(e)
                
                # Проверяем на ошибку invalid session (браузер закрылся)
                if "invalid session id" in error_str.lower():
                    logger.error(f"❌ Браузер был закрыт!")
                    logger.info("⚠️ Скрипт останавливается, так как браузер закрыт вручную или упал.")
                    update_parcel_status(parcel_id, "Прервано", "Браузер закрыт")
                    
                    # ОСТАНАВЛИВАЕМ СКРИПТ - не перезапускаем браузер
                    logger.info("🔚 Завершение работы...")
                    break  # Выходим из цикла обработки участков
                
                # Проверяем, это ошибка определения района или другая ошибка
                if "Район не определен" in error_str:
                    logger.error(f"❌ Район не определен для заявки {idx}: {error_str}")
                    update_parcel_status(parcel_id, "Район не определен", error_str)
                else:
                    logger.error(f"❌ Критическая ошибка для заявки {idx}: {e}")
                    update_parcel_status(parcel_id, "Ошибка", error_str)
                
                error_count += 1
                import traceback
                traceback.print_exc()
                
                # Пауза перед следующей заявкой
                if idx < len(parcels):
                    logger.info("⏳ Пауза 5 секунд перед следующей заявкой...")
                    time.sleep(5)
        
        # Итоговая статистика
        logger.info("\n" + "="*80)
        logger.info("🎉 ОБРАБОТКА ЗАВЕРШЕНА!")
        logger.info("="*80)
        logger.info(f"✅ Успешно отправлено заявлений: {success_count}")
        logger.info(f"🔒 Занятых участков (с обременениями): {occupied_count}")
        logger.info(f"🔍 Не найдено на Росреестре: {not_found_count}")
        logger.info(f"❌ Ошибок при отправке: {error_count}")
        logger.info(f"📊 Всего обработано участков: {len(parcels)}")
        logger.info("="*80)
        
        logger.info("\n⏳ Браузер останется открытым. Нажмите Ctrl+C для закрытия")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("\n🔚 Остановка по запросу пользователя...")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("🔚 Закрываю браузер...")
        driver.quit()

if __name__ == "__main__":
    main()

