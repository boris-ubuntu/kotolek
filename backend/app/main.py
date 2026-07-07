from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import transactions_router, categories_router

app = FastAPI(
    title="Котолёк API",
    description="API для управления семейным бюджетом",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions_router)
app.include_router(categories_router)

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
