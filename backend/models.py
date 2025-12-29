from pydantic import BaseModel
from typing import List


class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str


class IngredientsUser(BaseModel):
    available_ingredients: List[str]
