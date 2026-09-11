"""
recipe_agent_local.py
-----------------------
Local reference implementation of SmartRecipe AI's core logic, covering the
project's 8 core features end-to-end WITHOUT calling any model or spending
any coins:

  1. Ingredient-based recipe recommendations   -> score_recipe()
  2. Recipe retrieval from a knowledge base     -> retrieve_best_recipe()
  3. Dietary preference handling                -> score_recipe() diet filter
  4. Missing ingredient substitutions            -> flagged in the prompt for the model to fill in
  5. Serving-size adjustment                     -> scale_recipe.scale_ingredients()
  6. Step-by-step cooking instructions           -> pulled from the knowledge base
  7. Cooking tips                                -> pulled from the knowledge base
  8. Beginner-friendly responses                 -> enforced by system_prompt.txt

This script builds the exact prompt that Langflow's IBM watsonx.ai Model
component (running an IBM Granite model) would receive. Use it to verify
your retrieval and scaling logic for free before wiring up Langflow.
"""

import pandas as pd
from scale_recipe import scale_ingredients

SYSTEM_PROMPT = open("system_prompt.txt").read()


def load_recipes(path="data/recipes.csv"):
    return pd.read_csv(path)


def score_recipe(row, user_ingredients, diet_pref):
    recipe_ingredients = {i.split(":")[0].strip().lower() for i in row["ingredients"].split(",")}
    overlap = len(user_ingredients & recipe_ingredients)

    if diet_pref:
        tags = [t.strip().lower() for t in str(row["diet_tags"]).split(",")]
        if diet_pref.strip().lower() not in tags:
            return -1  # disqualified, doesn't meet dietary requirement

    return overlap


def retrieve_best_recipe(user_ingredients_str, diet_pref, df):
    user_set = {i.strip().lower() for i in user_ingredients_str.split(",") if i.strip()}
    df = df.copy()
    df["score"] = df.apply(lambda row: score_recipe(row, user_set, diet_pref), axis=1)
    df = df[df["score"] >= 0].sort_values("score", ascending=False)
    return df.iloc[0] if not df.empty else None


def missing_ingredients(user_ingredients_str, recipe_row):
    user_set = {i.strip().lower() for i in user_ingredients_str.split(",") if i.strip()}
    recipe_set = {i.split(":")[0].strip().lower() for i in recipe_row["ingredients"].split(",")}
    return sorted(recipe_set - user_set)


def build_prompt(user_ingredients_str, diet_pref, servings, recipe_row):
    scaled = scale_ingredients(recipe_row["ingredients"], int(recipe_row["base_servings"]), servings)
    missing = missing_ingredients(user_ingredients_str, recipe_row)
    missing_note = f"Missing from what the user has: {', '.join(missing)}. Suggest substitutions for these." \
        if missing else "The user already has everything needed."

    return f"""User's available ingredients: {user_ingredients_str}
Dietary preference: {diet_pref or "none"}
Requested servings: {servings}

Closest matching recipe from the knowledge base:
Name: {recipe_row['recipe_name']}
Cuisine: {recipe_row['cuisine']}
Ingredients (scaled to {servings} servings): {scaled}
Prep time: {recipe_row['prep_time']} | Cook time: {recipe_row['cook_time']}
Steps: {recipe_row['steps']}
Tip: {recipe_row['tips']}

{missing_note}

Using the system instructions, respond with the complete, structured recipe."""


if __name__ == "__main__":
    df = load_recipes()

    user_ingredients = input("What ingredients do you have? (comma-separated): ")
    diet_pref = input("Dietary preference (vegetarian/vegan/gluten-free/non-vegetarian/blank): ")
    servings = int(input("How many servings? ") or 2)

    best = retrieve_best_recipe(user_ingredients, diet_pref, df)

    if best is None:
        print("\nNo close match found. Try adding a common ingredient like rice, onion, or egg.")
    else:
        prompt = build_prompt(user_ingredients, diet_pref, servings, best)
        print("\n=== SYSTEM PROMPT (sent once) ===\n")
        print(SYSTEM_PROMPT)
        print("\n=== USER TURN (sent to IBM Granite via watsonx.ai) ===\n")
        print(prompt)
