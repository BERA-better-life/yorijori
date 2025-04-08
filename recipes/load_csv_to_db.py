import pandas as pd
from yourapp.models import Recipe, Ingredient, RecipeIngredient

# 파일 경로
recipes = pd.read_csv('recipes_table_0408.csv', encoding='utf-8-sig')
ingredients = pd.read_csv('ingredients_table_0408.csv', encoding='utf-8-sig')
recipe_ingredients = pd.read_csv('recipes_ingredients_0408.csv', encoding='utf-8-sig')

# 1. 재료 등록
for _, row in ingredients.iterrows():
    Ingredient.objects.get_or_create(ingredient_name=row['ingredient_name'])

# 2. 레시피 등록
for _, row in recipes.iterrows():
    Recipe.objects.get_or_create(rcp_number=row['rcp_number'], rcp_name=row['rcp_name'])

# 3. 레시피-재료 연결
for _, row in recipe_ingredients.iterrows():
    try:
        recipe = Recipe.objects.get(rcp_number=row['rcp_number'])
        ingredient = Ingredient.objects.get(ingredient_name=row['ingredient_name'])
        RecipeIngredient.objects.get_or_create(recipe=recipe, ingredient=ingredient)
    except Exception as e:
        print(f"에러: {e}")
