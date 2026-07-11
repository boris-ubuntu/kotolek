import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Transaction
from datetime import datetime
import random

def insert_data():
    db = SessionLocal()
    
    # Реалистичные данные по месяцам
    months_data = [
        (2026, 1, 80000, 80000),  # январь
        (2026, 2, 85000, 85000),  # февраль
        (2026, 3, 67000, 67000),  # март
        (2026, 4, 60000, 60000),  # апрель
        (2026, 5, 70000, 70000),  # май
        (2026, 6, 55000, 55000),  # июнь
    ]
    
    # Категории с реалистичными описаниями
    expense_details = {
        1: ['Продукты в магазине', 'Овощи и фрукты', 'Мясные продукты', 'Молочные продукты', 'Крупы и макароны'],
        2: ['Обед в кафе', 'Ужин в ресторане', 'Кофе с коллегами', 'Бизнес-ланч', 'Пицца'],
        3: ['Заправка АЗС', 'Топливо для авто', 'Бензин АИ-95', 'Дизельное топливо'],
        4: ['Мойка кузова', 'Химчистка салона', 'Полировка авто'],
        5: ['Замена масла', 'Техосмотр', 'Шиномонтаж', 'Замена фильтров', 'Ремонт подвески'],
        6: ['Покупка бытовой техники', 'Мебель', 'Посуда', 'Декор для дома'],
        7: ['Детские товары', 'Игрушки', 'Одежда для детей', 'Детское питание'],
        8: ['Одежда', 'Обувь', 'Аксессуары', 'Спортивная одежда'],
        9: ['Фитнес-клуб', 'Спортивные товары', 'Экипировка', 'Занятия спортом'],
        10: ['Билеты в театр', 'Кино', 'Музеи', 'Концерты'],
        11: ['Праздник', 'Торжество', 'Подарки', 'Мероприятие'],
        12: ['Оплата интернета', 'Мобильная связь', 'Хостинг', 'Подписки'],
        13: ['Штраф ГИБДД', 'Пени', 'Налог'],
        14: ['ЖКХ', 'Электричество', 'Вода', 'Отопление', 'Квартплата'],
        15: ['Проездной', 'Метро', 'Автобус', 'Такси'],
        16: ['Разное', 'Прочее', 'Непредвиденные расходы'],
    }
    
    for year, month, total_expense, total_income in months_data:
        # Расходы
        remaining = total_expense
        day = 1
        transaction_count = 0
        
        while remaining > 0 and day <= 28:
            # Выбираем категорию
            cat_id = random.choice(list(expense_details.keys()))
            desc_list = expense_details.get(cat_id, ['Расход'])
            description = random.choice(desc_list)
            
            # Реалистичные суммы
            if cat_id in [14, 1, 6]:  # ЖКХ, продукты, товары - крупные
                max_amount = min(20000, remaining)
                min_amount = min(1000, remaining)
            elif cat_id in [2, 3, 5]:  # Кафе, топливо, авто - средние
                max_amount = min(10000, remaining)
                min_amount = min(500, remaining)
            else:
                max_amount = min(5000, remaining)
                min_amount = min(300, remaining)
            
            if max_amount < min_amount:
                max_amount = remaining
                min_amount = remaining
            
            amount = random.randint(min_amount, max_amount) if min_amount < max_amount else max_amount
            
            if amount <= 0:
                break
            
            # Несколько транзакций в день
            hour = random.randint(8, 21)
            minute = random.randint(0, 59)
            
            txn = Transaction(
                amount=amount,
                category_id=cat_id,
                description=description,
                is_income=False,
                date=datetime(year, month, day, hour, minute)
            )
            db.add(txn)
            remaining -= amount
            transaction_count += 1
            
            # Переход к следующему дню
            if transaction_count % random.randint(2, 4) == 0:
                day += random.randint(1, 3)
                if day > 28:
                    break
        
        # Доходы (зарплата и дополнительные)
        if total_income > 0:
            # Основная зарплата 25 числа
            salary = int(total_income * 0.7)
            txn = Transaction(
                amount=salary,
                category_id=17,
                description='Зарплата за ' + datetime(year, month, 1).strftime('%B %Y'),
                is_income=True,
                date=datetime(year, month, 25, 9, 0)
            )
            db.add(txn)
            
            # Аванс 15 числа
            advance = int(total_income * 0.25)
            txn2 = Transaction(
                amount=advance,
                category_id=17,
                description='Аванс за ' + datetime(year, month, 1).strftime('%B %Y'),
                is_income=True,
                date=datetime(year, month, 15, 10, 0)
            )
            db.add(txn2)
            
            # Премия или подработка (не всегда)
            if random.random() > 0.4:
                bonus = random.randint(2000, 8000)
                txn3 = Transaction(
                    amount=bonus,
                    category_id=17,
                    description=random.choice(['Премия', 'Подработка', 'Возврат долга']),
                    is_income=True,
                    date=datetime(year, month, random.randint(20, 28), 12, 0)
                )
                db.add(txn3)
    
    db.commit()
    db.close()
    
    print("✅ Реалистичные тестовые данные добавлены!")
    print("")
    print("📊 Расходы по месяцам:")
    print("   Январь 2026:  80 000 ₽  (🔴 выше 75 000)")
    print("   Февраль 2026: 85 000 ₽  (🔴 выше 75 000)")
    print("   Март 2026:    67 000 ₽  (🟢 ниже 75 000)")
    print("   Апрель 2026:  60 000 ₽  (🟢 ниже 75 000)")
    print("   Май 2026:     70 000 ₽  (🟢 ниже 75 000)")
    print("   Июнь 2026:    55 000 ₽  (🟢 ниже 75 000)")
    print("")
    print("💰 Баланс по месяцам нулевой (доходы = расходы)")

if __name__ == "__main__":
    insert_data()
