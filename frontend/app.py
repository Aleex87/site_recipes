import streamlit as st
import requests

API_URL = "https://site-recipes-backend.onrender.com/recipes"

INGREDIENT_GROUPS = {
    "Pasta & Grains": [
        "spaghetti", "pasta", "rice", "noodles", "couscous"
    ],
    "Proteins": [
        "eggs", "chicken", "beef", "pork", "tofu",
        "beans", "lentils"
    ],
    "Dairy": [
        "milk", "butter", "cheese", "yogurt", "cream"
    ],
    "Vegetables": [
        "tomato", "potatoes", "onion", "garlic", "carrot",
        "zucchini", "pepper", "broccoli", "spinach", "lettuce"
    ],
    "Pantry": [
        "olive oil", "salt", "pepper", "water", "flour",
        "sugar", "vinegar", "soy sauce"
    ],
    "Herbs & Spices": [
        "basil", "oregano", "parsley", "paprika", "chili flakes"
    ],
    "Bakery": [
        "bread", "breadcrumbs", "yeast"
    ],
    "Extras": [
        "lemon", "mustard", "honey", "canned tomatoes", "stock"
    ]
}

st.title("Recipes from Your Fridge")

# -----------------------------
# Session state initialization
# -----------------------------
if "recipes" not in st.session_state:
    st.session_state.recipes = []

if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

st.subheader("Select the ingredients you have available")

selected_ingredients = []

# -----------------------------
# Checkbox grid by category
# -----------------------------
for group, items in INGREDIENT_GROUPS.items():
    st.markdown(f"### {group}")
    cols = st.columns(3)

    for i, item in enumerate(items):
        with cols[i % 3]:
            if st.checkbox(item, key=f"{group}_{item}"):
                selected_ingredients.append(item)

st.divider()

# -----------------------------
# Fetch recipes
# -----------------------------
if st.button("Find recipes"):
    if not selected_ingredients:
        st.warning("Please select at least one ingredient.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"available_ingredients": selected_ingredients},
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)
            else:
                st.session_state.recipes = response.json()
                st.session_state.selected_recipe = None

        except Exception as e:
            st.error("Exception while calling backend")
            st.text(str(e))

# -----------------------------
# Show results
# -----------------------------
if st.session_state.recipes:
    st.success(f"Found {len(st.session_state.recipes)} recipes")

    recipe_names = [r["name"] for r in st.session_state.recipes]

    selected_name = st.selectbox(
        "Select a recipe to see details",
        recipe_names
    )

    st.session_state.selected_recipe = next(
        r for r in st.session_state.recipes
        if r["name"] == selected_name
    )

    r = st.session_state.selected_recipe

    st.subheader(r["name"])

    st.markdown("**Ingredients:**")
    for ing in r["ingredients"]:
        st.write(f"- {ing}")

    st.markdown("**You have:**")
    for ing in r["matched_ingredients"]:
        st.write(f"✅ {ing}")

    if r["missing_ingredients"]:
        st.markdown("**You are missing:**")
        for ing in r["missing_ingredients"]:
            st.write(f"❌ {ing}")

    st.markdown("**Instructions:**")
    st.write(r["instructions"])
