import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .config import Config
from .core.rate_limiter import limiter

# Import routers after limiter is defined
from .routers import transactions_router, categories_router
# auth_router imported later to avoid circular import

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title="Котолёк API",
    description="API для управления семейным бюджетом",
    version="1.0.0",
    lifespan=lifespan
)

# Rate limiter exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration - restrict to specific origins in production
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
    if not Config.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

app.include_router(transactions_router)
app.include_router(categories_router)

# Import auth_router here to avoid circular import
from .routers.auth import router as auth_router
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в Котолёк API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
