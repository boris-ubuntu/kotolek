from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)

@router.get("/recent")
def get_recent_transactions(
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return crud.get_recent_transactions(db, limit)

@router.get("/balance")
def get_balance(db: Session = Depends(get_db)):
    return crud.get_balance(db)

@router.get("/expenses-by-category")
def get_expenses_by_category(db: Session = Depends(get_db)):
    return crud.get_expenses_by_category(db)

@router.get("/daily-balance")
def get_daily_balance(db: Session = Depends(get_db)):
    return crud.get_daily_balance(db)

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_transaction(db, transaction_id)
