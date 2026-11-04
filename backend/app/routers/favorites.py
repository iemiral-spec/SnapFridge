"""Favoriler. Sahibi: Umut (WBS-5.2). Her kullanıcı sadece kendi favorilerini görür."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Favorite, Recipe, User
from ..schemas import RecipeSummary
from ..security import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=list[RecipeSummary])
def list_favorites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favs = db.scalars(select(Favorite).where(Favorite.user_id == user.id).order_by(Favorite.created_at.desc())).all()
    return [RecipeSummary(id=f.recipe.id, title=f.recipe.title, image_url=f.recipe.image_url) for f in favs]


@router.put("/{recipe_id}", status_code=204)
def add_favorite(recipe_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.get(Recipe, recipe_id) is None:
        raise HTTPException(404, "Tarif bulunamadı.")
    exists = db.scalar(select(Favorite).where(Favorite.user_id == user.id, Favorite.recipe_id == recipe_id))
    if exists is None:  # PUT idempotent: ikinci kez eklemek hata vermez, kopya oluşturmaz
        db.add(Favorite(user_id=user.id, recipe_id=recipe_id))
        db.commit()
    return Response(status_code=204)


@router.delete("/{recipe_id}", status_code=204)
def remove_favorite(recipe_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fav = db.scalar(select(Favorite).where(Favorite.user_id == user.id, Favorite.recipe_id == recipe_id))
    if fav is not None:
        db.delete(fav)
        db.commit()
    return Response(status_code=204)
