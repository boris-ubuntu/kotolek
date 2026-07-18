import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Если задана переменная DATABASE_URL — используем её, иначе собираем из компонентов
    _database_url = os.getenv("DATABASE_URL")
    if _database_url:
        DATABASE_URL = _database_url
    else:
        DB_USER = os.getenv("POSTGRES_USER")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        DB_HOST = os.getenv("DB_HOST", "db")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("POSTGRES_DB")
        if not all([DB_USER, DB_PASSWORD, DB_NAME]):
            raise ValueError("POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB must be set")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    # SECRET_KEY берётся из переменной окружения. Если она не задана (например,
    # Render не сгенерировал значение), используем запасной ключ, чтобы приложение
    # не падало при импорте или запуске. В продакшене рекомендуется задать
    # собственный надёжный SECRET_KEY через переменные окружения.
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "kotolek-fallback-secret-key-change-me-in-production-7f3a9c2d",
    )
