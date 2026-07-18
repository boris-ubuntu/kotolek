from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models import User
from ..auth import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    get_current_user, 
    verify_token
)
from ..core.rate_limiter import limiter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(request: Request, data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неверный логин или пароль"
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return schemas.Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        username=user.username, 
        token_type="bearer",
        expires_in=30 * 60  # 30 minutes in seconds
    )


@router.post("/refresh", response_model=schemas.Token)
@limiter.limit("10/minute")
def refresh_token(request: Request, data: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    username = verify_token(data.refresh_token, "refresh")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истекший refresh токен"
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return schemas.Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        username=user.username, 
        token_type="bearer",
        expires_in=30 * 60
    )


@router.post("/register", response_model=schemas.UserOut)
def register(data: schemas.UserCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    exists = db.query(User).filter(User.username == data.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=schemas.UserOut)
def me(user: User = Depends(get_current_user)):
    return user