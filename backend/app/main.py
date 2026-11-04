"""SnapFridge API giriş noktası. Çalıştırma: `uvicorn app.main:app --reload` (backend/ klasöründe)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, SessionLocal, engine
from .routers import admin, auth, favorites, ingredients, recipes
from .services.recipes import seed_common_ingredients


@asynccontextmanager
async def lifespan(app: FastAPI):
    # İlk sürümde tablolar otomatik oluşturulur. Şema değişmeye başlayınca
    # Alembic migration'a geçilmesi önerilir (İdil / Ahmet İlker).
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed_common_ingredients(db)
    yield


app = FastAPI(title="SnapFridge API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, ingredients, recipes, favorites, admin):
    app.include_router(r.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
