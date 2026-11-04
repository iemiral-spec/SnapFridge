"""Örnek tarifleri yükler (veri seti gelene kadar geliştirme için).

Kullanım (backend/ klasöründe): python -m scripts.seed_sample
"""
import json
from pathlib import Path

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Recipe
from app.schemas import RecipeIn
from app.services.recipes import apply_recipe_data, seed_common_ingredients


def main() -> None:
    Base.metadata.create_all(engine)
    data = json.loads((Path(__file__).parent / "sample_recipes.json").read_text(encoding="utf-8"))
    with SessionLocal() as db:
        seed_common_ingredients(db)
        added = 0
        for item in data:
            if db.scalar(select(Recipe).where(Recipe.title == item["title"])):
                continue
            recipe = Recipe(source="sample")
            db.add(recipe)
            apply_recipe_data(db, recipe, RecipeIn(**item))
            added += 1
        db.commit()
    print(f"{added} örnek tarif eklendi.")


if __name__ == "__main__":
    main()
