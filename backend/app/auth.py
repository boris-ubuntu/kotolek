import hmac
import hashlib
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .config import Config

_SECRET = Config.SECRET_KEY.encode("utf-8") if isinstance(Config.SECRET_KEY, str) else Config.SECRET_KEY

_bearer = HTTPBearer(auto_error=False)


def hash_password(password):
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return "pbkdf2:" + salt.hex() + ":" + dk.hex()


def verify_password(password, password_hash):
    try:
        if not password_hash.startswith("pbkdf2:"):
            return False
        _, salt_hex, dk_hex = password_hash.split(":", 2)
        salt = bytes.fromhex(salt_hex)
        dk = bytes.fromhex(dk_hex)
        new_dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(new_dk, dk)
    except Exception:
        return False


def create_token(username):
    sig = hmac.new(_SECRET, username.encode("utf-8"), hashlib.sha256).hexdigest()
    raw = username + "::" + sig
    return raw.encode("utf-8").hex()


def verify_token(token):
    try:
        raw = bytes.fromhex(token).decode("utf-8")
        username, sig = raw.split("::", 1)
        expected = hmac.new(_SECRET, username.encode("utf-8"), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, sig):
            return username
    except Exception:
        return None
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer), db: Session = Depends(get_db)):
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация", headers={"WWW-Authenticate": "Bearer"})
    username = verify_token(credentials.credentials)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен", headers={"WWW-Authenticate": "Bearer"})
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден", headers={"WWW-Authenticate": "Bearer"})
    return user