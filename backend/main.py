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

    matching_recipes = []

    for recipe in recipes_db:
        if set(recipe.ingredients).issubset(user_ingredients):
            matching_recipes.append(recipe)

    return matching_recipes
