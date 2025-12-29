from models import Recipe, IngredientsUser

recipe = Recipe(
    name="Pasta al pomodoro",
    ingredients=["pasta", "pomodoro", "olio"],
    instructions="Cuoci la pasta e preprara il sugo."
)
print(recipe)
print(type(recipe))

# test imput 

user_input = IngredientsUser(
    available_ingredients=["uova", "latte"]
)

print(user_input)