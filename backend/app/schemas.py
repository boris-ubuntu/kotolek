from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    color: str
    is_income: bool = False
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    category_id: int
    description: Optional[str] = None
    is_income: bool = False

class TransactionCreate(TransactionBase):
    date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    amount: float
    category_id: int
    category_name: str
    category_color: str
    description: Optional[str] = None
    is_income: bool
    date: str
    created_at: str

class BalanceResponse(BaseModel):
    balance: float
    month_income: float
    month_expenses: float

class CategoryExpense(BaseModel):
    name: str
    color: str
    total: float

class DailyBalance(BaseModel):
    date: str
    balance: float

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    username: str
    expires_in: int  # seconds

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
