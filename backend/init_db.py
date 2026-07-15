import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Category, User
from app.auth import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_categories(db):
    categories_data = [
        # Еда (#5390d9)
        {"name": "Продукты", "color": "#5390d9", "is_income": False},
        {"name": "Кафе", "color": "#5390d9", "is_income": False},
        # Авто (#56cfe1)
        {"name": "Топливо", "color": "#56cfe1", "is_income": False},
        {"name": "Мойка", "color": "#56cfe1", "is_income": False},
        {"name": "Тех. обслуживание", "color": "#56cfe1", "is_income": False},
        # Товары (#5e60ce)
        {"name": "Товары", "color": "#5e60ce", "is_income": False},
        {"name": "Дети", "color": "#5e60ce", "is_income": False},
        {"name": "Одежда", "color": "#5e60ce", "is_income": False},
        # Мероприятия (#6930c3)
        {"name": "Спорт", "color": "#6930c3", "is_income": False},
        {"name": "Культура", "color": "#6930c3", "is_income": False},
        {"name": "События", "color": "#6930c3", "is_income": False},
        # Платежи (#2acbcb)
        {"name": "Интернет", "color": "#2acbcb", "is_income": False},
        {"name": "Штрафы", "color": "#2acbcb", "is_income": False},
        {"name": "ЖКХ", "color": "#2acbcb", "is_income": False},
        {"name": "Общественный транспорт", "color": "#2acbcb", "is_income": False},
        {"name": "Прочее", "color": "#2acbcb", "is_income": False},
        # Доход (#4ea8de)
        {"name": "Доход", "color": "#4ea8de", "is_income": True},
    ]
    
    for cat_data in categories_data:
        exists = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not exists:
            category = Category(**cat_data)
            db.add(category)
            logger.info(f"Добавлена категория: {cat_data['name']}")
    
    db.commit()
    logger.info("Все категории успешно добавлены!")

def init_users(db):
    users_data = [
        {"username": "boris", "password": "Maelstormer5"},
        {"username": "test", "password": "test"},
    ]
    for u in users_data:
        exists = db.query(User).filter(User.username == u["username"]).first()
        if not exists:
            user = User(username=u["username"], password_hash=hash_password(u["password"]))
            db.add(user)
            logger.info(f"Добавлен пользователь: {u['username']}")
        else:
            logger.info(f"Пользователь уже существует: {u['username']}")
    db.commit()

def main():
    logger.info("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        logger.info("Инициализация пользователей...")
        init_users(db)
        logger.info("Инициализация категорий...")
        init_categories(db)
        logger.info("Инициализация базы данных завершена успешно!")
    except Exception as e:
        logger.error(f"Ошибка при инициализации: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
