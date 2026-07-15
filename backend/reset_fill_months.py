"""
Сбрасывает и заново заполняет последние 3 месяца окна (Ноя 2025, Дек 2025, Янв 2026)
сбалансированными демо-данными, чтобы гистограмма из 9 месяцев выглядела
аккуратно и без выбивающихся значений.
"""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Transaction
from sqlalchemy import and_
from datetime import datetime


def main():
    db = SessionLocal()

    # Границы сбрасываемого диапазона
    start = datetime(2025, 11, 1)
    end = datetime(2026, 1, 31, 23, 59, 59)

    old = db.query(Transaction).filter(
        and_(Transaction.date >= start, Transaction.date <= end)
    ).delete()
    print(f"Удалено старых записей в диапазоне: {old}")

    # (год, месяц, зарплата, целевая сумма расходов)
    plan = [
        (2025, 11, 70000, 65000),
        (2025, 12, 75000, 70000),
        (2026, 1, 72000, 68000),
    ]

    expense_cats = [1, 3, 6, 12, 14, 16]
    added = 0

    for year, month, salary, target in plan:
        db.add(Transaction(
            amount=salary,
            category_id=17,
            description='Зарплата за ' + datetime(year, month, 1).strftime('%B %Y'),
            is_income=True,
            date=datetime(year, month, 25, 9, 0),
        ))
        added += 1

        remaining = target
        day = 2
        while remaining > 0 and day <= 27:
            cat = random.choice(expense_cats)
            amt = min(remaining, random.randint(3000, 12000))
            if amt <= 0:
                break
            db.add(Transaction(
                amount=amt,
                category_id=cat,
                description=None,
                is_income=False,
                date=datetime(year, month, day, 12, 0),
            ))
            added += 1
            remaining -= amt
            day += random.randint(2, 4)

    db.commit()
    print(f"✅ Добавлено новых транзакций: {added}")
    db.close()


if __name__ == "__main__":
    main()