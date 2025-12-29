import json
import random
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
SEED = 42
NUM_RECIPES = 300

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "backend" / "data" / "recipes.json"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

random.seed(SEED)

# -----------------------------
# Ingredient pools (English)
# Keep these broadly aligned with your Streamlit checkbox groups.
# -----------------------------
PASTA_RICE = ["spaghetti", "pasta", "rice", "noodles", "couscous"]
PROTEINS = ["eggs", "chicken", "beef", "pork", "tofu", "beans", "lentils"]
DAIRY = ["milk", "butter", "cheese", "yogurt", "cream"]
VEGETABLES = ["tomato", "potatoes", "onion", "garlic", "carrot", "zucchini", "pepper", "broccoli", "spinach", "lettuce"]
PANTRY = ["olive oil", "salt", "pepper", "water", "flour", "sugar", "vinegar", "soy sauce"]
HERBS_SPICES = ["basil", "oregano", "parsley", "paprika", "chili flakes"]
BAKERY = ["bread", "breadcrumbs", "yeast"]

# Optional: extra “common” items for more variety (still simple)
EXTRAS = ["lemon", "mustard", "honey", "canned tomatoes", "stock"]

ALL = list(dict.fromkeys(PASTA_RICE + PROTEINS + DAIRY + VEGETABLES + PANTRY + HERBS_SPICES + BAKERY + EXTRAS))

# -----------------------------
# Instruction templates
# (A bit detailed, but not overly long)
# -----------------------------
def steps_for_pasta(main, veg, protein, dairy, pantry, spice):
    return (
        f"Bring a large pot of salted water to a boil and cook the {main} until al dente. "
        f"Meanwhile, heat {pantry} in a pan over medium heat and sauté {veg} until softened. "
        f"Add {protein} and cook until done, then season with {spice}. "
        f"Drain the {main}, toss it in the pan, and finish with {dairy}. Serve hot."
    )

def steps_for_rice(main, veg, protein, dairy, pantry, spice):
    return (
        f"Rinse the {main} if needed, then cook it in salted water until tender. "
        f"In a separate pan, warm {pantry} and sauté {veg} until fragrant. "
        f"Add {protein} and cook through, then season with {spice}. "
        f"Fold the cooked {main} into the pan and stir well. "
        f"Finish with {dairy} for extra richness and serve."
    )

def steps_for_stirfry(veg, protein, pantry, spice):
    return (
        f"Heat {pantry} in a hot pan or wok. Add {veg} and stir-fry for 3–5 minutes. "
        f"Add {protein} and continue cooking until fully done. "
        f"Season with {spice} and adjust salt and pepper to taste. Serve immediately."
    )

def steps_for_soup(veg1, veg2, protein, pantry, spice):
    return (
        f"Warm {pantry} in a pot and sauté {veg1} for 2–3 minutes. "
        f"Add {veg2} and stir for another minute, then pour in water (or stock if available). "
        f"Add {protein} and simmer gently for 15–25 minutes until everything is tender. "
        f"Season with {spice} and salt to taste. Rest for 2 minutes before serving."
    )

def steps_for_sandwich(bread, protein, dairy, veg, pantry):
    return (
        f"Lightly toast the {bread} if you want extra crunch. "
        f"Layer {protein}, {dairy}, and {veg}. "
        f"Add a small amount of {pantry} for moisture and flavor, then close and slice. Serve right away."
    )

def steps_for_bake(veg, protein, pantry, spice):
    return (
        f"Preheat the oven to 200°C. Toss {veg} with {pantry} and season with {spice} and salt. "
        f"Add {protein} and spread everything on a baking tray. "
        f"Bake for 20–35 minutes (depending on thickness) until browned and cooked through. Serve hot."
    )

def steps_for_breakfast(protein, dairy, pantry, spice):
    return (
        f"Heat {pantry} in a pan over low-to-medium heat. "
        f"Add {protein} and cook gently, stirring when needed. "
        f"Finish with {dairy} and season with {spice} and salt. Serve warm."
    )

# -----------------------------
# Recipe builders
# -----------------------------
def unique_name(base, used_names):
    if base not in used_names:
        used_names.add(base)
        return base
    i = 2
    while f"{base} #{i}" in used_names:
        i += 1
    name = f"{base} #{i}"
    used_names.add(name)
    return name

def pick_one(pool):
    return random.choice(pool)

def pick_two(pool):
    a = random.choice(pool)
    b = random.choice([x for x in pool if x != a])
    return a, b

def maybe_add(ingredients, item, prob=0.35):
    if random.random() < prob and item not in ingredients:
        ingredients.append(item)

def build_pasta_recipe(used_names):
    main = pick_one(["spaghetti", "pasta", "noodles"])
    veg = pick_one(["tomato", "onion", "garlic", "pepper", "zucchini", "spinach"])
    protein = pick_one(["eggs", "chicken", "tofu", "beans", "lentils"])
    dairy = pick_one(["cheese", "butter", "cream", "yogurt"])
    pantry = pick_one(["olive oil", "soy sauce", "vinegar"])
    spice = pick_one(["basil", "oregano", "parsley", "paprika", "chili flakes", "pepper"])

    ingredients = [main, veg, protein, dairy, pantry, "salt"]
    maybe_add(ingredients, "pepper", 0.55)
    maybe_add(ingredients, "garlic", 0.30)

    base_name = f"{main.title()} with {veg.title()} and {protein.title()}"
    name = unique_name(base_name, used_names)

    instructions = steps_for_pasta(main, veg, protein, dairy, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_rice_recipe(used_names):
    main = pick_one(["rice", "couscous"])
    veg = pick_one(["carrot", "onion", "pepper", "broccoli", "spinach", "tomato"])
    protein = pick_one(["eggs", "chicken", "tofu", "beans", "lentils", "beef"])
    dairy = pick_one(["butter", "cheese", "yogurt", "cream"])
    pantry = pick_one(["olive oil", "soy sauce", "vinegar"])
    spice = pick_one(["parsley", "paprika", "chili flakes", "pepper", "oregano"])

    ingredients = [main, veg, protein, dairy, pantry, "salt"]
    maybe_add(ingredients, "garlic", 0.40)
    maybe_add(ingredients, "onion", 0.25)

    base_name = f"{main.title()} Bowl with {veg.title()} and {protein.title()}"
    name = unique_name(base_name, used_names)

    instructions = steps_for_rice(main, veg, protein, dairy, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_stirfry_recipe(used_names):
    veg1, veg2 = pick_two(["onion", "garlic", "carrot", "pepper", "broccoli", "zucchini", "spinach"])
    veg = f"{veg1} and {veg2}"
    protein = pick_one(["chicken", "beef", "pork", "tofu", "beans"])
    pantry = pick_one(["olive oil", "soy sauce"])
    spice = pick_one(["chili flakes", "paprika", "pepper", "parsley"])

    ingredients = [protein, veg1, veg2, pantry, "salt"]
    maybe_add(ingredients, "pepper", 0.60)
    maybe_add(ingredients, "soy sauce", 0.35)
    maybe_add(ingredients, "olive oil", 0.35)

    base_name = f"{protein.title()} Stir-Fry with {veg1.title()} and {veg2.title()}"
    name = unique_name(base_name, used_names)

    instructions = steps_for_stirfry(veg, protein, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_soup_recipe(used_names):
    veg1 = pick_one(["onion", "garlic", "carrot", "tomato"])
    veg2 = pick_one(["potatoes", "broccoli", "spinach", "zucchini"])
    protein = pick_one(["beans", "lentils", "chicken", "tofu"])
    pantry = pick_one(["olive oil", "butter"])
    spice = pick_one(["parsley", "oregano", "pepper", "paprika"])

    ingredients = [veg1, veg2, protein, pantry, "water", "salt"]
    maybe_add(ingredients, "stock", 0.20)  # from EXTRAS
    maybe_add(ingredients, "pepper", 0.60)

    base_name = f"{veg2.title()} and {protein.title()} Soup"
    name = unique_name(base_name, used_names)

    instructions = steps_for_soup(veg1, veg2, protein, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_sandwich_recipe(used_names):
    bread = pick_one(["bread"])
    protein = pick_one(["eggs", "chicken", "tofu", "cheese"])
    dairy = pick_one(["cheese", "butter", "yogurt"])
    veg = pick_one(["lettuce", "tomato", "onion"])
    pantry = pick_one(["olive oil", "mustard", "vinegar"])

    ingredients = [bread, protein, dairy, veg, "salt"]
    maybe_add(ingredients, pantry, 0.85)
    maybe_add(ingredients, "pepper", 0.40)

    base_name = f"{protein.title()} and {veg.title()} Sandwich"
    name = unique_name(base_name, used_names)

    instructions = steps_for_sandwich(bread, protein, dairy, veg, pantry)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_bake_recipe(used_names):
    veg = pick_one(["potatoes", "carrot", "pepper", "zucchini", "broccoli"])
    protein = pick_one(["chicken", "tofu", "pork"])
    pantry = pick_one(["olive oil", "butter"])
    spice = pick_one(["paprika", "oregano", "pepper", "chili flakes"])

    ingredients = [veg, protein, pantry, "salt"]
    maybe_add(ingredients, "garlic", 0.35)
    maybe_add(ingredients, "onion", 0.25)

    base_name = f"Oven-Baked {protein.title()} with {veg.title()}"
    name = unique_name(base_name, used_names)

    instructions = steps_for_bake(veg, protein, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

def build_breakfast_recipe(used_names):
    protein = pick_one(["eggs"])
    dairy = pick_one(["cheese", "butter", "milk", "cream"])
    pantry = pick_one(["butter", "olive oil"])
    spice = pick_one(["pepper", "chili flakes", "parsley"])

    ingredients = [protein, dairy, pantry, "salt"]
    maybe_add(ingredients, "bread", 0.35)
    maybe_add(ingredients, "tomato", 0.25)

    base_name = f"Quick {protein.title()} with {dairy.title()}"
    name = unique_name(base_name, used_names)

    instructions = steps_for_breakfast(protein, dairy, pantry, spice)
    return {"name": name, "ingredients": ingredients, "instructions": instructions}

BUILDERS = [
    build_pasta_recipe,
    build_rice_recipe,
    build_stirfry_recipe,
    build_soup_recipe,
    build_sandwich_recipe,
    build_bake_recipe,
    build_breakfast_recipe,
]

# -----------------------------
# Generate recipes
# -----------------------------
def normalize_ingredients(ingredients):
    # Deduplicate while preserving order
    seen = set()
    out = []
    for x in ingredients:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out

def main():
    used_names = set()
    recipes = []

    # Generate until we have NUM_RECIPES unique names
    attempts = 0
    max_attempts = NUM_RECIPES * 20

    while len(recipes) < NUM_RECIPES and attempts < max_attempts:
        attempts += 1
        builder = random.choice(BUILDERS)
        r = builder(used_names)

        r["ingredients"] = normalize_ingredients(r["ingredients"])

        # Basic sanity: ensure ingredients are known (except stock which we allow)
        for ing in r["ingredients"]:
            if ing != "stock" and ing not in ALL:
                # If unknown, skip recipe
                break
        else:
            recipes.append(r)

    if len(recipes) < NUM_RECIPES:
        raise RuntimeError(f"Could only generate {len(recipes)} recipes after {attempts} attempts.")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(recipes)} recipes -> {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
