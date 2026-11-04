"""Tarif eşleştirme ve detay. Sahibi: İdil (WBS-4.1)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recipe
from ..schemas import MatchIn, RecipeDetail, RecipeMatch
from ..services.matching import RecipeLike, match_recipes
from ..services.recipes import to_detail

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


@router.post("/match", response_model=list[RecipeMatch])
def match(body: MatchIn, db: Session = Depends(get_db)):
    # Basit ilk sürüm: tüm tarifler belleğe alınır. Veri seti birkaç yüz tarif
    # olduğu sürece yeterli; büyürse SQL tarafında ön filtre eklenecek.
    recipes = db.scalars(select(Recipe)).all()
    candidates = [
        RecipeLike(r.id, r.title, [ri.ingredient.name for ri in r.ingredients], r.image_url) for r in recipes
    ]
    return [RecipeMatch(**m.__dict__) for m in match_recipes(body.ingredients, candidates)]


@router.get("/{recipe_id}", response_model=RecipeDetail)
def detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(404, "Tarif bulunamadı.")
    return to_detail(recipe)
