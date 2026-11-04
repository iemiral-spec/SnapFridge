"""Malzeme listesi ve fotoğraf analizi.

- GET  /api/ingredients/common : seçim ekranındaki etiketler (Talha/İdil)
- GET  /api/ingredients/search : arama kutusu (İdil)
- POST /api/recognize          : fotoğraf yükleme (Biray, WBS-3.1) + tanıma (Talha, WBS-3.2)
"""
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..ingredients_list import COMMON_INGREDIENTS, normalize
from ..models import Ingredient, User
from ..schemas import RecognitionOut
from ..security import get_current_user
from ..services.vision import VisionError, get_provider

router = APIRouter(prefix="/api", tags=["ingredients"])

ALLOWED_TYPES = {"image/jpeg", "image/png"}


@router.get("/ingredients/common", response_model=list[str])
def common_ingredients():
    return COMMON_INGREDIENTS


@router.get("/ingredients/search", response_model=list[str])
def search_ingredients(q: str = Query(min_length=1, max_length=50), db: Session = Depends(get_db)):
    term = normalize(q)
    names = db.scalars(
        select(Ingredient.name).where(Ingredient.name.contains(term)).order_by(Ingredient.name).limit(20)
    ).all()
    return list(names)


@router.post("/recognize", response_model=RecognitionOut)
async def recognize(photo: UploadFile = File(...), user: User = Depends(get_current_user)):
    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, "Sadece JPEG veya PNG fotoğraf yükleyebilirsiniz.")
    data = await photo.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "Fotoğraf 10 MB'den büyük olamaz.")
    if not data:
        raise HTTPException(400, "Fotoğraf boş.")
    # Fotoğraf kaydedilmez; sadece bellekte işlenir (plan: images are transient).
    try:
        provider = get_provider()
        result = provider.recognize(data, photo.content_type)
    except VisionError as exc:
        raise HTTPException(502, f"{exc} Malzemeleri listeden elle seçebilirsiniz.")
    return RecognitionOut(**result, demo=provider.is_demo)
