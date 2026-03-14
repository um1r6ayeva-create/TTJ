import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.api import router as api_v1_router
from app.db.session import engine
from app.db.base_class import Base
from app.db.init_db import init_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

# Создаем таблицы если их нет (для простоты деплоя в Neon)
try:
    Base.metadata.create_all(bind=engine)
    init_db()
except Exception as e:
    print(f"Error initializing DB: {e}")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- CORS middleware должно идти до include_router ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIR),
    name="uploads"
)

# Подключаем роутеры
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/api/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get("/api/init-db")
def trigger_init_db():
    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        # Инициализируем данные
        init_db()
        return {"status": "success", "message": "Database initialized and tables created"}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

@app.get("/api/health")
def health_check():
    import traceback
    from sqlalchemy import text
    try:
        # Пытаемся подключиться к БД
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            # Получаем список таблиц
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            
        return {
            "status": "healthy", 
            "db_connected": True, 
            "tables": tables,
            "registered_models": list(Base.metadata.tables.keys())
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "db_connected": False, 
            "error": str(e),
            "traceback": traceback.format_exc()
        }