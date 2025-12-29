from fastapi import FastAPI
from backend.models import Recipe, IngredientsUser
import json
from pathlib import Path

app = FastAPI()

DATA_PATH = Path(__file__).parent / "data" / "recipes.json"


def load_recipes() -> list[Recipe]:
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [Recipe(**recipe) for recipe in data]


recipes_db = load_recipes()

@app.get("/")
def root():
    return {
        "message": "Recipe API is running",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.post("/recipes")
def suggest_recipes(user: IngredientsUser):
    user_ingredients = set(user.available_ingredients)
    results = []

    for recipe in recipes_db:
        recipe_ingredients = set(recipe.ingredients)
        matched = recipe_ingredients.intersection(user_ingredients)
        missing = recipe_ingredients - user_ingredients

        if matched:
            results.append({
                "name": recipe.name,
                "ingredients": recipe.ingredients,
                "instructions": recipe.instructions,
                "matched_ingredients": list(matched),
                "missing_ingredients": list(missing)
            })

    results.sort(key=lambda r: len(r["matched_ingredients"]), reverse=True)

    return results


