from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import io
import csv
import codecs
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

@router.get("/by-month")
def get_transactions_by_month(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return crud.get_transactions_by_month(db, year, month)

@router.get("/balance")
def get_balance(db: Session = Depends(get_db)):
    return crud.get_balance(db)

@router.get("/expenses-by-category")
def get_expenses_by_category(db: Session = Depends(get_db)):
    return crud.get_expenses_by_category(db)

@router.get("/daily-balance")
def get_daily_balance(db: Session = Depends(get_db)):
    return crud.get_daily_balance(db)

@router.get("/monthly-expenses")
def get_monthly_expenses(db: Session = Depends(get_db)):
    return crud.get_monthly_expenses(db)

@router.get("/month-summary")
def get_month_summary(db: Session = Depends(get_db)):
    return crud.get_month_summary(db)

@router.get("/export")
def export_transactions(db: Session = Depends(get_db)):
    try:
        # Экспортируем всё без ограничения
        all_transactions = crud.get_all_transactions(db, skip=0, limit=10_000_000)
        
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        
        writer.writerow(['id', 'amount', 'category_id', 'category_name', 'description', 'is_income', 'date', 'created_at'])
        
        for txn in all_transactions:
            writer.writerow([
                txn['id'],
                txn['amount'],
                txn['category_id'],
                txn['category_name'],
                txn['description'] if txn['description'] else '',
                str(txn['is_income']),
                txn['date'],
                txn['created_at']
            ])
        
        output.seek(0)
        
        filename = f"kotolek_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return Response(
            content=output.getvalue().encode('utf-8-sig'),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "text/csv; charset=utf-8-sig"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Только CSV файлы")
    
    content = await file.read()
    decoded = content.decode('utf-8-sig')
    lines = decoded.splitlines()
    
    reader = csv.reader(lines, delimiter=';')
    
    try:
        headers = next(reader)
    except StopIteration:
        raise HTTPException(status_code=400, detail="Пустой файл")
    
    imported = 0
    skipped = 0
    
    for row in reader:
        try:
            if len(row) < 8:
                skipped += 1
                continue
            
            amount = float(row[1].replace(',', '.'))
            category_id = int(row[2])
            is_income = row[5].strip().lower() == 'true'
            date = datetime.fromisoformat(row[6]) if row[6] else datetime.now()
            
            transaction_data = schemas.TransactionCreate(
                amount=amount,
                category_id=category_id,
                description=row[4] if len(row) > 4 and row[4] else None,
                is_income=is_income,
                date=date
            )
            
            # Пропускаем уже существующие записи — защита от дубликатов
            result = crud.create_transaction(db, transaction_data, skip_duplicates=True)
            if result is None:
                skipped += 1
            else:
                imported += 1
            
        except Exception as e:
            skipped += 1
            continue
    
    return JSONResponse({
        "imported": imported,
        "skipped": skipped,
        "message": f"Импортировано {imported} записей, пропущено {skipped}"
    })

@router.post("/dedupe")
def dedupe_transactions(db: Session = Depends(get_db)):
    """Удаляет существующие дубликаты в базе данных."""
    try:
        removed = crud.dedupe_transactions(db)
        return JSONResponse({
            "removed": removed,
            "message": f"Удалено дубликатов: {removed}"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_transaction(db, transaction_id)
