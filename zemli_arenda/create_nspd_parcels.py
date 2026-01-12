#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическое создание земельных участков через Selenium на НСПД
"""

import time
import logging
from datetime import datetime
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
        logging.FileHandler('nspd_parcels.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URL НСПД
NSPD_URL = "https://nspd.gov.ru"

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
    
    chrome_options = Options()
    
    # Headless режим
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    else:
        chrome_options.add_argument("--start-maximized")
    
    # Общие настройки
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Блокируем popup окна и новые вкладки
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.popups": 2,
        "profile.popup_exceptions": {},
    })
    
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
                if i > 0:
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

def authorize_gosuslugi(driver, wait, headless=False):
    """
    Авторизация на Госуслугах
    
    Args:
        driver: WebDriver
        wait: WebDriverWait
        headless: Режим headless
    
    Returns:
        bool: True если авторизация успешна
    """
    logger.info("\n🔐 Начало авторизации на Госуслугах...")
    
    try:
        driver.get("https://www.gosuslugi.ru")
        time.sleep(3)
        
        # Проверяем, авторизован ли уже
        try:
            user_menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Меню пользователя')]")
            logger.info("✅ Пользователь уже авторизован")
            return True
        except:
            logger.warning("⚠️ Пользователь не авторизован, выполняю вход...")
        
        # Ждём полной загрузки страницы
        logger.info("   ⏳ Жду загрузки главной страницы...")
        time.sleep(3)
        
        # Сохраняем скриншот для отладки
        if headless:
            try:
                driver.save_screenshot("debug_gosuslugi_main.png")
                logger.info("   📸 Скриншот: debug_gosuslugi_main.png")
            except:
                pass
        
        # Ищем кнопку "Войти"
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
        time.sleep(5)
        
        # Ждем появления поля логина
        logger.info("   🔍 Ищу форму логина...")
        
        if headless:
            try:
                driver.save_screenshot("debug_gosuslugi_login_form.png")
                logger.info("   📸 Скриншот: debug_gosuslugi_login_form.png")
            except:
                pass
        
        login_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='login' or @type='tel' or @id='login']"))
        )
        logger.info("   ✅ Форма логина найдена")
        current_login = login_field.get_attribute('value') or ''
        
        if '+79295154970' in current_login:
            logger.info("✅ Логин уже подставлен, ввожу только пароль")
            password_field = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='password' or @type='password']"))
            )
            password_field.clear()
            password_field.send_keys("_4_BW:%rcn6")
            logger.info("   Пароль введен")
            time.sleep(2)
        else:
            logger.info("📝 Ввожу логин и пароль")
            login_field.clear()
            login_field.send_keys("+79295154970")
            logger.info("   Логин введен")
            time.sleep(2)
            
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
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(0.5)
            submit_button.click()
            logger.info("   ✅ Кнопка входа нажата")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"   ⚠️ Не удалось нажать кнопку входа автоматически: {e}")
            logger.info("   👉 НАЖМИТЕ КНОПКУ 'ВОЙТИ' ВРУЧНУЮ")
        
        # Ждем SMS код
        if headless:
            logger.info("📱 Ожидаю ввода SMS-кода...")
            logger.info("   SMS-код будет отправлен на номер +79295154970")
            time.sleep(5)
            
            sms_code = input("\n👉 Введите SMS-код: ").strip()
            
            if sms_code:
                logger.info(f"   Получен код: {sms_code}")
                
                try:
                    sms_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @inputmode='numeric' or contains(@placeholder, 'код')]"))
                    )
                    sms_field.clear()
                    sms_field.send_keys(sms_code)
                    logger.info("   ✅ SMS-код введён")
                    time.sleep(1)
                    
                    try:
                        confirm_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти') or contains(., 'Подтвердить')]"))
                        )
                        driver.execute_script("arguments[0].click();", confirm_button)
                        logger.info("   ✅ Кнопка подтверждения нажата")
                        time.sleep(3)
                    except:
                        logger.warning("   ⚠️ Кнопка подтверждения не найдена")
                    
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
                return False
        else:
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
        
        # Обработка выбора профиля
        logger.info("\n🔍 Проверка необходимости выбора профиля...")
        time.sleep(2)
        
        try:
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
            profile_button = driver.find_element(By.XPATH, "//button[contains(., 'Абрамян') or contains(., 'частное лицо') or contains(., 'Частное лицо')]")
            logger.info("   👤 Найдена кнопка выбора профиля")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_button)
            time.sleep(0.5)
            profile_button.click()
            logger.info("   ✅ Выбран профиль 'Частное лицо'")
            time.sleep(2)
        except:
            logger.info("   ℹ️  Выбор профиля не требуется (уже выбран)")
        
        logger.info("✅ Авторизация на Госуслугах завершена\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при авторизации: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_parcel_on_nspd(driver, wait, parcel_data):
    """
    Создать земельный участок на НСПД
    
    Args:
        driver: WebDriver
        wait: WebDriverWait
        parcel_data: Данные участка (dict)
    
    Returns:
        bool: True если успешно создан
    """
    logger.info(f"\n📝 Создание участка: {parcel_data.get('cadastral_number', 'Нет КН')}")
    
    try:
        # TODO: Здесь будет логика создания участка на НСПД
        # После авторизации через Госуслуги переходим на НСПД
        
        logger.info(f"   Переход на НСПД: {NSPD_URL}")
        driver.get(NSPD_URL)
        time.sleep(3)
        
        # Сохраняем скриншот
        driver.save_screenshot(f"nspd_main_page.png")
        logger.info(f"   📸 Скриншот: nspd_main_page.png")
        
        # Здесь будут шаги по заполнению формы создания участка
        # Пока оставляем заглушку для тестирования авторизации
        
        logger.info("✅ Участок создан (тестовый режим)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при создании участка: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"error_create_parcel.png")
        return False

def main():
    """Главная функция"""
    logger.info("="*80)
    logger.info("🚀 СОЗДАНИЕ ЗЕМЕЛЬНЫХ УЧАСТКОВ НА НСПД")
    logger.info("="*80)
    
    # Запрашиваем режим запуска браузера
    print("\n" + "-"*80)
    print("🖥️  РЕЖИМ ЗАПУСКА БРАУЗЕРА")
    print("-"*80)
    print("1. Обычный режим (с видимым окном Chrome)")
    print("2. Фоновый режим (headless, без GUI)")
    print("-"*80)
    
    headless_choice = input("👉 Ваш выбор (1 или 2, Enter = обычный): ").strip()
    
    if headless_choice == "2":
        headless_mode = True
        print("✅ Выбран фоновый режим (headless)")
    else:
        headless_mode = False
        print("✅ Выбран обычный режим")
    
    # Настройка браузера
    driver = setup_browser(headless=headless_mode)
    wait = WebDriverWait(driver, 45)
    
    try:
        # Авторизация через Госуслуги
        if not authorize_gosuslugi(driver, wait, headless=headless_mode):
            logger.error("❌ Не удалось авторизоваться. Завершение работы.")
            return
        
        # Тестовые данные участка
        test_parcel = {
            'cadastral_number': '74:00:0000000:0000',
            'address': 'Тестовый адрес',
            'area': 1000
        }
        
        # Создание участка
        success = create_parcel_on_nspd(driver, wait, test_parcel)
        
        if success:
            logger.info("\n✅ Участок успешно создан!")
        else:
            logger.error("\n❌ Не удалось создать участок")
        
        # Итоговая статистика
        logger.info("\n" + "="*80)
        logger.info("🎉 РАБОТА ЗАВЕРШЕНА!")
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







