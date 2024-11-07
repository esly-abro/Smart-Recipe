import pandas as pd

csv_url_1 = 'https://drive.google.com/uc?id=10vuvzzDJ_Bypyt7XJVeHVgzeXolcDyCL'
recipes_df_1 = pd.read_csv(csv_url_1)

csv_url_3 = 'https://drive.google.com/uc?id=13apn07VxfvJKbNVogjL2ATJ93I20Oo9D'
recipes_df_3 = pd.read_csv(csv_url_3)

recipes_df_1.columns = recipes_df_1.columns.str.strip()
recipes_df_3.columns = recipes_df_3.columns.str.strip()

recipes_df_1.rename(columns={
    'Unnamed: 0': 'Index',
    'Title': 'RecipeName',
    'Ingredients': 'Ingredients',
    'Instructions': 'Instructions',
    'Image_Name': 'ImageURL',
    'Cleaned_Ingredients': 'CleanedIngredients'
}, inplace=True)

recipes_df_3.rename(columns={
    'TranslatedRecipeName': 'RecipeName',
    'TranslatedIngredients': 'CleanedIngredients',
    'TranslatedInstructions': 'Instructions',
    'image-url': 'ImageURL'
}, inplace=True)

common_columns = ['RecipeName', 'CleanedIngredients', 'Instructions']
combined_recipes_df = pd.concat(
    [
        recipes_df_1[common_columns],
        recipes_df_3[common_columns]
    ],
    ignore_index=True
)

def find_recipes(available_ingredients):
    matched_recipes = []
    for _, row in combined_recipes_df.iterrows():
        recipe_ingredients = [ingredient.strip().lower() for ingredient in row['CleanedIngredients'].split(',')]
        if all(item in recipe_ingredients for item in available_ingredients):
            matched_recipes.append({
                "RecipeName": row['RecipeName'],
                "CleanedIngredients": row['CleanedIngredients'],
                "Instructions": row['Instructions']
            })
    return matched_recipes

user_input = input("Enter excess food items you have (comma-separated): ")
available_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(',')]

suggested_recipes = find_recipes(available_ingredients)

if suggested_recipes:
    print("\nHere are some recipes you can make with your excess food:\n")
    for recipe in suggested_recipes:
        print(f"Recipe: {recipe['RecipeName']}")
        print(f"Ingredients: {recipe['CleanedIngredients']}")
        print(f"Instructions: {recipe['Instructions']}\n")
        print("-" * 40 + "\n")  # Line divider between recipes
else:
    print("\nSorry, no matching recipes found.")
