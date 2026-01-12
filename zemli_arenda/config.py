"""
Конфигурация системы "Фабрика участков"
"""
import os
from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).parent

# База данных
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "parcels.db"))

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

# Веб-интерфейс
WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("WEB_PORT", "8080"))
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Создание необходимых директорий
(BASE_DIR / "data").mkdir(exist_ok=True)
(BASE_DIR / "logs").mkdir(exist_ok=True)
(BASE_DIR / "exports").mkdir(exist_ok=True)















