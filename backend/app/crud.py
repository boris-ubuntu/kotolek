from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from . import models, schemas
from fastapi import HTTPException

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
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

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Транзакция удалена"}

def get_recent_transactions(db: Session, limit: int = 5):
    results = db.query(
        models.Transaction,
        models.Category.name.label('category_name'),
        models.Category.color.label('category_color')
    ).join(
        models.Category,
        models.Transaction.category_id == models.Category.id
    ).order_by(
        models.Transaction.date.desc()
    ).limit(limit).all()
    
    transactions = []
    for row in results:
        txn = row[0]
        transactions.append({
            "id": txn.id,
            "amount": txn.amount,
            "category_id": txn.category_id,
            "category_name": row.category_name,
            "category_color": row.category_color,
            "description": txn.description,
            "is_income": txn.is_income,
            "date": txn.date.isoformat(),
            "created_at": txn.created_at.isoformat()
        })
    return transactions

def get_transactions_by_month(db: Session, year: int, month: int):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    results = db.query(
        models.Transaction,
        models.Category.name.label('category_name'),
        models.Category.color.label('category_color')
    ).join(
        models.Category,
        models.Transaction.category_id == models.Category.id
    ).filter(
        models.Transaction.date >= start_date,
        models.Transaction.date <= end_date
    ).order_by(
        models.Transaction.date.desc()
    ).all()
    
    transactions = []
    for row in results:
        txn = row[0]
        transactions.append({
            "id": txn.id,
            "amount": txn.amount,
            "category_id": txn.category_id,
            "category_name": row.category_name,
            "category_color": row.category_color,
            "description": txn.description,
            "is_income": txn.is_income,
            "date": txn.date.isoformat(),
            "created_at": txn.created_at.isoformat()
        })
    return transactions

def get_balance(db: Session):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1)
    
    month_income = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.is_income == True,
            models.Transaction.date >= start_date
        )
    ).scalar() or 0.0
    
    month_expenses = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.is_income == False,
            models.Transaction.date >= start_date
        )
    ).scalar() or 0.0
    
    balance = month_income - month_expenses
    
    return {
        "balance": balance,
        "month_income": month_income,
        "month_expenses": month_expenses
    }

def get_expenses_by_category(db: Session):
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

def get_daily_balance(db: Session):
    now = datetime.now()
    start_date = datetime(now.year, now.month, 1)
    end_date = now
    
    transactions = db.query(
        models.Transaction.date,
        models.Transaction.amount,
        models.Transaction.is_income
    ).filter(
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

def get_monthly_expenses(db: Session):
    now = datetime.now()
    months = []
    
    for i in range(6):
        month_date = now - timedelta(days=30*i)
        month_start = datetime(month_date.year, month_date.month, 1)
        if i == 0:
            month_end = now
        else:
            next_month = month_start.replace(day=28) + timedelta(days=4)
            month_end = next_month - timedelta(days=next_month.day)
        
        total = db.query(func.sum(models.Transaction.amount)).filter(
            and_(
                models.Transaction.is_income == False,
                models.Transaction.date >= month_start,
                models.Transaction.date <= month_end
            )
        ).scalar() or 0.0
        
        months.append({
            "month": month_start.strftime("%b"),
            "year": month_start.year,
            "total": float(total),
            "color": "#e53e3e" if total > 75000 else "#48bb78"
        })
    
    return months[::-1]
