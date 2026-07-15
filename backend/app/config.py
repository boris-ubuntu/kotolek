import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Если задана переменная DATABASE_URL — используем её, иначе собираем из компонентов
    _database_url = os.getenv("DATABASE_URL")
    if _database_url:
        DATABASE_URL = _database_url
    else:
        DB_USER = os.getenv("POSTGRES_USER", "kotolek")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "kotolek")
        DB_HOST = os.getenv("DB_HOST", "db")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("POSTGRES_DB", "kotolek")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
