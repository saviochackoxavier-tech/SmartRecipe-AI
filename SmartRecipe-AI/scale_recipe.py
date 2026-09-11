"""
scale_recipe.py
----------------
Custom component for the Thai Recipe Agent.

Purpose: given a recipe's ingredient list (as stored in thai_recipes.csv,
formatted as "name:quantity unit, name:quantity unit, ..."), scale every
quantity proportionally to a new number of servings.

This is intentionally small and dependency-free so it is cheap to generate
and verify with an AI coding assistant (e.g. IBM Bob) in a single focused
task, and easy to drop into a Langflow flow as a Custom Component (Python
function) between the recipe-retrieval step and the prompt sent to the
IBM Granite model.

Example
-------
>>> scale_ingredients("shrimp or tofu:150g, egg:2, lime:1", base_servings=2, target_servings=5)
'shrimp or tofu: 375.0g, egg: 5.0, lime: 2.5'
"""

import re


def _parse_amount(raw: str):
    """Split '150g' -> (150.0, 'g'); '2' -> (2.0, ''); '1 cup' -> (1.0, 'cup')."""
    raw = raw.strip()
    match = re.match(r"^([\d.]+)\s*(.*)$", raw)
    if not match:
        # No leading number found (e.g. "a pinch") - leave untouched
        return None, raw
    value, unit = match.groups()
    return float(value), unit.strip()


def scale_ingredients(ingredients_str: str, base_servings: int, target_servings: int) -> str:
    """
    ingredients_str: "name:qty unit, name:qty unit, ..." as stored in the CSV
    base_servings:   the serving size the recipe was originally written for
    target_servings: the serving size requested by the user
    """
    if base_servings <= 0:
        raise ValueError("base_servings must be greater than 0")

    factor = target_servings / base_servings
    scaled_items = []

    for item in ingredients_str.split(","):
        if ":" not in item:
            scaled_items.append(item.strip())
            continue
        name, raw_amount = item.split(":", 1)
        value, unit = _parse_amount(raw_amount)
        if value is None:
            # Can't scale a non-numeric amount (e.g. "a pinch") - keep as-is
            scaled_items.append(f"{name.strip()}: {raw_amount.strip()}")
            continue
        scaled_raw = round(value * factor, 2)
        scaled_value = int(scaled_raw) if scaled_raw == int(scaled_raw) else scaled_raw
        scaled_items.append(f"{name.strip()}: {scaled_value}{unit}")

    return ", ".join(scaled_items)


if __name__ == "__main__":
    sample = "rice noodles:200g, shrimp or tofu:150g, egg:2, lime:1"
    print("Original (serves 2):", sample)
    print("Scaled to 5 servings:", scale_ingredients(sample, base_servings=2, target_servings=5))
