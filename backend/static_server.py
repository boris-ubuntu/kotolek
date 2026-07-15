import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.routers.categories import router as categories_router
from app.routers.transactions import router as transactions_router
from app.database import engine, Base

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("⚠️ Таблицы ещё не созданы (БД возможно не готова), продолжим после init_db:", e)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return JSONResponse(
        content={},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

app.include_router(categories_router)
app.include_router(transactions_router)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/test")
def test():
    return {"message": "API работает!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"🚀 Сервер запущен на http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
