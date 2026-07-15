"""
Импорт данных из CSV-экспорта Котолёк в базу данных.
Использует ту же логику разбора, что и эндпоинт /api/transactions/import.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import csv
from datetime import datetime
from app.database import SessionLocal
from app import schemas, crud, models


def import_csv(path: str):
    db = SessionLocal()
    imported = 0
    skipped = 0
    try:
        # Идемпотентность: не импортируем, если в БД уже есть транзакции
        existing = db.query(models.Transaction).first()
        if existing is not None:
            print("ℹ️ Транзакции уже присутствуют в БД, импорт пропущен (во избежание дублей)")
            return

        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            try:
                headers = next(reader)
            except StopIteration:
                print("Пустой файл")
                return

            for row in reader:
                try:
                    if len(row) < 8:
                        skipped += 1
                        continue

                    amount = float(row[1].replace(",", "."))
                    category_id = int(row[2])
                    is_income = row[5].strip().lower() == "true"
                    date = datetime.fromisoformat(row[6]) if row[6] else datetime.now()

                    transaction_data = schemas.TransactionCreate(
                        amount=amount,
                        category_id=category_id,
                        description=row[4] if len(row) > 4 and row[4] else None,
                        is_income=is_income,
                        date=date,
                    )

                    # Пропускаем уже существующие записи — защита от дублей
                    result = crud.create_transaction(db, transaction_data, skip_duplicates=True)
                    if result is None:
                        skipped += 1
                    else:
                        imported += 1
                except Exception as e:
                    skipped += 1
                    print(f"⚠️ Пропущена строка: {row[:3]} — {e}")
                    continue

        print(f"✅ Импортировано {imported} записей, пропущено {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kotolek_export.csv")
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    if not os.path.exists(path):
        print(f"❌ Файл не найден: {path}")
        sys.exit(1)
    import_csv(path)