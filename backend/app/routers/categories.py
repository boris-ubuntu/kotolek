from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=List[schemas.Category])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получить список всех категорий
    """
    return crud.get_categories(db, skip, limit)

@router.get("/{category_id}", response_model=schemas.Category)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить категорию по ID
    """
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category
