"""TheMealDB tariflerini veritabanına aktarır. Sahibi: İdil (WBS-2.2).

Kullanım (backend/ klasöründe): python -m scripts.import_themealdb
Not: TheMealDB'nin ücretsiz test anahtarı ("1") geliştirme/eğitim içindir.
Lisans ve atıf şartları raporda kontrol edilip yazılmalı (plan: Assumptions).
"""
import string

import httpx
from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.ingredients_list import normalize
from app.models import Recipe
from app.schemas import RecipeIn, RecipeIngredientOut
from app.services.recipes import apply_recipe_data, seed_common_ingredients

API = "https://www.themealdb.com/api/json/v1/1/search.php"


def meal_to_recipe(meal: dict) -> RecipeIn | None:
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip()
        if name:
            ingredients.append(RecipeIngredientOut(name=normalize(name), measure=(meal.get(f"strMeasure{i}") or "").strip()))
    if not ingredients:
        return None
    return RecipeIn(
        title=meal["strMeal"],
        instructions=meal.get("strInstructions") or "",
        image_url=meal.get("strMealThumb"),
        ingredients=ingredients,
    )


def main() -> None:
    Base.metadata.create_all(engine)
    added = 0
    with httpx.Client(timeout=20) as client, SessionLocal() as db:
        seed_common_ingredients(db)
        for letter in string.ascii_lowercase:
            meals = client.get(API, params={"f": letter}).json().get("meals") or []
            for meal in meals:
                if db.scalar(select(Recipe).where(Recipe.source == "themealdb", Recipe.source_id == meal["idMeal"])):
                    continue
                data = meal_to_recipe(meal)
                if data is None:
                    continue
                recipe = Recipe(source="themealdb", source_id=meal["idMeal"])
                db.add(recipe)
                apply_recipe_data(db, recipe, data)
                added += 1
            db.commit()
    print(f"{added} tarif TheMealDB'den eklendi.")


if __name__ == "__main__":
    main()
