from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import calendar
from . import models, schemas
from fastapi import HTTPException


# ========== Вспомогательные функции ==========

def _build_transaction_response(row):
    """Преобразует строку результата JOIN-запроса в словарь."""
    txn = row[0]
    return {
        "id": txn.id,
        "amount": txn.amount,
        "category_id": txn.category_id,
        "category_name": row.category_name,
        "category_color": row.category_color,
        "description": txn.description,
        "is_income": txn.is_income,
        "date": txn.date.isoformat(),
        "created_at": txn.created_at.isoformat(),
    }


def _get_transactions_query(db: Session):
    """Базовый JOIN-запрос транзакций с категориями — устраняет дублирование."""
    return db.query(
        models.Transaction,
        models.Category.name.label("category_name"),
        models.Category.color.label("category_color"),
    ).join(
        models.Category,
        models.Transaction.category_id == models.Category.id,
    )


# ========== Категории ==========

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

# ========== Транзакции ==========

def _validate_category_exists(db: Session, category_id: int):
    """Проверяет, что категория существует — предотвращает битые ссылки."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=400,
            detail=f"Категория с id={category_id} не найдена",
        )


def transaction_exists(db: Session, amount, category_id, is_income, date_from, date_to, description, user_id):
    """Проверяет, есть ли уже такая транзакция (по сигнатуре) — борьба с дублями (в рамках пользователя)."""
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.amount == amount,
        models.Transaction.category_id == category_id,
        models.Transaction.is_income == is_income,
        models.Transaction.date >= date_from,
        models.Transaction.date < date_to,
    )
    if description:
        query = query.filter(models.Transaction.description == description)
    else:
        query = query.filter(models.Transaction.description.is_(None))
    return query.first() is not None


def dedupe_transactions(db: Session, user_id: int = None):
    """Удаляет существующие дубликаты по сигнатуре amount+category_id+is_income+date+description (в рамках пользователя)."""
    q = db.query(models.Transaction)
    if user_id is not None:
        q = q.filter(models.Transaction.user_id == user_id)
    rows = q.order_by(models.Transaction.id).all()
    seen = set()
    removed = 0
    for t in rows:
        key = (t.user_id, round(float(t.amount), 2), t.category_id, t.is_income, t.date, t.description)
        if key in seen:
            db.delete(t)
            removed += 1
        else:
            seen.add(key)
    db.commit()
    return removed


def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int, skip_duplicates: bool = False):
    if skip_duplicates:
        effective_date = transaction.date or datetime.now()
        day_start = effective_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = effective_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        if transaction_exists(
            db,
            transaction.amount,
            transaction.category_id,
            transaction.is_income,
            day_start,
            day_end,
            transaction.description,
            user_id,
        ):
            return None
    _validate_category_exists(db, transaction.category_id)
    db_transaction = models.Transaction(
        user_id=user_id,
        amount=transaction.amount,
        category_id=transaction.category_id,
        description=transaction.description,
        is_income=transaction.is_income,
        date=transaction.date or datetime.now()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id,
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Транзакция удалена"}

def get_all_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return [
        _build_transaction_response(r)
        for r in _get_transactions_query(db)
        .filter(models.Transaction.user_id == user_id)
        .order_by(models.Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    ]


def get_recent_transactions(db: Session, user_id: int, limit: int = 5):
    return [
        _build_transaction_response(r)
        for r in _get_transactions_query(db)
        .filter(models.Transaction.user_id == user_id)
        .order_by(models.Transaction.date.desc())
        .limit(limit)
        .all()
    ]


def get_transactions_by_month(db: Session, user_id: int, year: int, month: int):
    start_date = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day, 23, 59, 59)

    return [
        _build_transaction_response(r)
        for r in _get_transactions_query(db)
        .filter(
            models.Transaction.user_id == user_id,
            models.Transaction.date >= start_date,
            models.Transaction.date <= end_date,
        )
        .order_by(models.Transaction.date.desc())
        .all()
    ]

def get_balance(db: Session, user_id: int):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1)
    
    stats = db.query(
        func.coalesce(
            func.sum(models.Transaction.amount).filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == True,
                    models.Transaction.date >= start_date,
                )
            ),
            0.0,
        ).label("month_income"),
        func.coalesce(
            func.sum(models.Transaction.amount).filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == False,
                    models.Transaction.date >= start_date,
                )
            ),
            0.0,
        ).label("month_expenses"),
    ).first()

    month_income = float(stats.month_income)
    month_expenses = float(stats.month_expenses)

    return {
        "balance": round(month_income - month_expenses, 2),
        "month_income": month_income,
        "month_expenses": month_expenses,
    }

def get_expenses_by_category(db: Session, user_id: int):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1)
    
    results = db.query(
        models.Category.name,
        models.Category.color,
        func.sum(models.Transaction.amount).label('total')
    ).join(
        models.Transaction,
        models.Transaction.category_id == models.Category.id
    ).filter(
        and_(
            models.Transaction.user_id == user_id,
            models.Transaction.is_income == False,
            models.Transaction.date >= start_date
        )
    ).group_by(
        models.Category.id
    ).all()
    
    return [
        {
            "name": r.name,
            "color": r.color,
            "total": float(r.total)
        }
        for r in results
    ]

def get_daily_balance(db: Session, user_id: int):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1)
    end_date = now
    
    transactions = db.query(
        models.Transaction.date,
        models.Transaction.amount,
        models.Transaction.is_income
    ).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.date >= start_date,
        models.Transaction.date <= end_date
    ).order_by(
        models.Transaction.date.asc()
    ).all()
    
    daily = {}
    for t in transactions:
        date_key = t.date.strftime("%Y-%m-%d")
        if date_key not in daily:
            daily[date_key] = 0
        if t.is_income:
            daily[date_key] += t.amount
        else:
            daily[date_key] -= t.amount
    
    result = []
    cumulative = 0
    current = start_date
    
    while current <= end_date:
        date_key = current.strftime("%Y-%m-%d")
        cumulative += daily.get(date_key, 0)
        result.append({
            "date": date_key,
            "balance": cumulative
        })
        current += timedelta(days=1)
    
    return result

def get_month_summary(db: Session, user_id: int):
    """Сводка по текущему месяцу: самый крупный расход и сравнение
    с предыдущим месяцем в процентах (в рамках пользователя)."""
    now = datetime.now()
    cur_start = datetime(now.year, now.month, 1)
    _, cur_last = calendar.monthrange(now.year, now.month)
    cur_end = datetime(now.year, now.month, cur_last, 23, 59, 59)

    if now.month == 1:
        prev_year, prev_month = now.year - 1, 12
    else:
        prev_year, prev_month = now.year, now.month - 1
    prev_start = datetime(prev_year, prev_month, 1)
    _, prev_last = calendar.monthrange(prev_year, prev_month)
    prev_end = datetime(prev_year, prev_month, prev_last, 23, 59, 59)

    def month_expense(start, end):
        return float(
            db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
            .filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == False,
                    models.Transaction.date >= start,
                    models.Transaction.date <= end,
                )
            )
            .scalar()
        )

    def top_expense(start, end):
        row = (
            db.query(
                models.Transaction.id,
                models.Transaction.amount,
                models.Transaction.description,
                models.Transaction.date,
                models.Category.name.label("category_name"),
                models.Category.color.label("category_color"),
            )
            .join(models.Category, models.Transaction.category_id == models.Category.id)
            .filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == False,
                    models.Transaction.date >= start,
                    models.Transaction.date <= end,
                )
            )
            .order_by(models.Transaction.amount.desc())
            .first()
        )
        if row is None:
            return 0.0, None
        detail = {
            "id": row.id,
            "amount": float(row.amount),
            "description": row.description,
            "date": row.date.isoformat(),
            "category_name": row.category_name,
            "category_color": row.category_color,
        }
        return float(row.amount), detail

    def month_income(start, end):
        return float(
            db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
            .filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == True,
                    models.Transaction.date >= start,
                    models.Transaction.date <= end,
                )
            )
            .scalar()
        )

    cur_expense = month_expense(cur_start, cur_end)
    prev_expense = month_expense(prev_start, prev_end)
    top, top_detail = top_expense(cur_start, cur_end)
    income = month_income(cur_start, cur_end)

    pct = None
    if prev_expense > 0:
        pct = round((cur_expense - prev_expense) / prev_expense * 100, 1)

    return {
        "top_expense": top,
        "top_expense_detail": top_detail,
        "current_month_expense": cur_expense,
        "previous_month_expense": prev_expense,
        "current_month_income": income,
        "change_pct": pct,
    }


def get_monthly_expenses(db: Session, user_id: int):
    """Последние 9 месяцев с корректным расчётом (без дрейфа timedelta) — в рамках пользователя."""
    now = datetime.now()
    months = []

    for i in range(8, -1, -1):
        total_months = now.year * 12 + (now.month - 1) - i
        year = total_months // 12
        month = total_months % 12 + 1

        month_start = datetime(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        month_end = datetime(year, month, last_day, 23, 59, 59)

        total = (
            db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
            .filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.is_income == False,
                    models.Transaction.date >= month_start,
                    models.Transaction.date <= month_end,
                )
            )
            .scalar()
        )

        months.append(
            {
                "month": month_start.strftime("%b"),
                "year": month_start.year,
                "total": float(total),
                "color": "#f27362" if float(total) >= 75000 else "#00aff5",
            }
        )

    return months
