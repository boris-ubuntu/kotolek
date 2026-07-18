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
        {"username": "test", "password": "test123"},
    ]
    for u in users_data:
        exists = db.query(User).filter(User.username == u["username"]).first()
        if not exists:
            user = User(username=u["username"], password_hash=hash_password(u["password"]))
            db.add(user)
            logger.info(f"Добавлен пользователь: {u['username']}")
        else:
            # Обновляем пароль, чтобы изменения входили в силу при повторном деплое
            exists.password_hash = hash_password(u["password"])
            logger.info(f"Пользователь уже существует, пароль обновлён: {u['username']}")
    db.commit()

def add_user_id_column(db):
    """Добавляем колонку user_id в transactions, если её ещё нет
    (create_all не добавляет колонки в уже существующие таблицы)."""
    from sqlalchemy import inspect, text
    inspector = inspect(db.bind)
    columns = [c["name"] for c in inspector.get_columns("transactions")]
    if "user_id" not in columns:
        db.execute(text("ALTER TABLE transactions ADD COLUMN user_id INTEGER REFERENCES users(id)"))
        db.commit()
        logger.info("Добавлена колонка transactions.user_id")
    else:
        logger.info("Колонка transactions.user_id уже существует")

def backfill_transactions_owner(db):
    """Существующие транзакции без user_id привязываем к boris (основной пользователь).
    Новые транзакции всегда создаются с user_id, поэтому test остаётся пустым."""
    from app.models import Transaction
    boris = db.query(User).filter(User.username == "boris").first()
    if not boris:
        logger.warning("boris не найден — пропуск привязки транзакций")
        return
    orphan_count = db.query(Transaction).filter(Transaction.user_id.is_(None)).count()
    if orphan_count > 0:
        db.query(Transaction).filter(Transaction.user_id.is_(None)).update(
            {Transaction.user_id: boris.id}
        )
        db.commit()
        logger.info(f"Привязано транзакций к boris: {orphan_count}")
    else:
        logger.info("Все транзакции уже привязаны к пользователям")

def main():
    logger.info("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        logger.info("Инициализация пользователей...")
        init_users(db)
        logger.info("Инициализация категорий...")
        init_categories(db)
        logger.info("Добавление колонки user_id в transactions...")
        add_user_id_column(db)
        logger.info("Привязка существующих транзакций к пользователю...")
        backfill_transactions_owner(db)
        logger.info("Инициализация базы данных завершена успешно!")
    except Exception as e:
        logger.error(f"Ошибка при инициализации: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
