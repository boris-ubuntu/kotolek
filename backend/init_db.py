import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Category
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_categories(db):
    categories_data = [
        # Расходы (красный)
        {"name": "Продукты", "color": "#FF0000", "is_income": False},
        {"name": "Кафе", "color": "#FF0000", "is_income": False},
        # Расходы (фиолетовый)
        {"name": "Топливо", "color": "#8B00FF", "is_income": False},
        {"name": "Мойка", "color": "#8B00FF", "is_income": False},
        {"name": "Тех. обслуживание", "color": "#8B00FF", "is_income": False},
        # Расходы (голубой)
        {"name": "Товары", "color": "#00BFFF", "is_income": False},
        {"name": "Дети", "color": "#00BFFF", "is_income": False},
        {"name": "Одежда", "color": "#00BFFF", "is_income": False},
        # Расходы (зеленый)
        {"name": "Спорт", "color": "#00FF00", "is_income": False},
        {"name": "Культура", "color": "#00FF00", "is_income": False},
        {"name": "События", "color": "#00FF00", "is_income": False},
        # Расходы (оранжевый)
        {"name": "Интернет", "color": "#FF8C00", "is_income": False},
        {"name": "Штрафы", "color": "#FF8C00", "is_income": False},
        {"name": "ЖКХ", "color": "#FF8C00", "is_income": False},
        {"name": "Общественный транспорт", "color": "#FF8C00", "is_income": False},
        {"name": "Прочее", "color": "#FF8C00", "is_income": False},
        # Доход (желтый)
        {"name": "Доход", "color": "#FFD700", "is_income": True},
    ]
    
    for cat_data in categories_data:
        exists = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not exists:
            category = Category(**cat_data)
            db.add(category)
            logger.info(f"Добавлена категория: {cat_data['name']}")
    
    db.commit()
    logger.info("Все категории успешно добавлены!")

def main():
    logger.info("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
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
