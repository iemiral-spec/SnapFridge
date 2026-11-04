"""Admin tarif yönetimi. Sahibi: İdil (WBS-6.1). Sadece is_admin=True kullanıcılar."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recipe
from ..schemas import RecipeDetail, RecipeIn
from ..security import require_admin
from ..services.recipes import apply_recipe_data, to_detail

router = APIRouter(prefix="/api/admin/recipes", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("", response_model=RecipeDetail, status_code=201)
def create_recipe(body: RecipeIn, db: Session = Depends(get_db)):
    recipe = Recipe(source="manual")
    db.add(recipe)
    apply_recipe_data(db, recipe, body)
    db.commit()
    return to_detail(recipe)


@router.put("/{recipe_id}", response_model=RecipeDetail)
def update_recipe(recipe_id: int, body: RecipeIn, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(404, "Tarif bulunamadı.")
    apply_recipe_data(db, recipe, body)
    db.commit()
    return to_detail(recipe)


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(404, "Tarif bulunamadı.")
    db.delete(recipe)
    db.commit()
    return Response(status_code=204)
