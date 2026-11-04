"""Tarif kayıt yardımcıları (içe aktarma, admin ve API ortak kullanır). Sahibi: İdil."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..ingredients_list import COMMON_INGREDIENTS, canonical, normalize
from ..models import Ingredient, Recipe, RecipeIngredient
from ..schemas import RecipeDetail, RecipeIngredientOut, RecipeIn


def get_or_create_ingredient(db: Session, name: str) -> Ingredient:
    name = canonical(name)
    ing = db.scalar(select(Ingredient).where(Ingredient.name == name))
    if ing is None:
        ing = Ingredient(name=name, is_common=name in COMMON_INGREDIENTS)
        db.add(ing)
        db.flush()
    return ing


def seed_common_ingredients(db: Session) -> None:
    for name in COMMON_INGREDIENTS:
        get_or_create_ingredient(db, name)
    db.commit()


def apply_recipe_data(db: Session, recipe: Recipe, data: RecipeIn) -> Recipe:
    recipe.title = data.title
    recipe.instructions = data.instructions
    recipe.image_url = data.image_url
    recipe.ingredients.clear()
    db.flush()
    seen: set[int] = set()
    for item in data.ingredients:
        ing = get_or_create_ingredient(db, item.name)
        if ing.id in seen:
            continue
        seen.add(ing.id)
        label = normalize(item.label or item.name)
        recipe.ingredients.append(
            RecipeIngredient(ingredient=ing, measure=item.measure, label=label if label != ing.name else "")
        )
    return recipe


def to_detail(recipe: Recipe) -> RecipeDetail:
    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        image_url=recipe.image_url,
        instructions=recipe.instructions,
        source=recipe.source,
        ingredients=[RecipeIngredientOut(name=ri.ingredient.name, measure=ri.measure, label=ri.label) for ri in recipe.ingredients],
    )
