# Contributing to SmartRecipe AI

Thanks for your interest in improving SmartRecipe AI! This is a small
student project, so contributions are kept intentionally simple.

## Ways to contribute

- **Add recipes** to `data/recipes.csv` (please keep the existing column
  format: `recipe_name, cuisine, base_servings, diet_tags, ingredients,
  prep_time, cook_time, steps, tips`, with ingredients as `name:quantity
  unit`).
- **Improve the system prompt** in `system_prompt.txt` for clearer, more
  helpful responses.
- **Fix bugs** in `scale_recipe.py` or `recipe_agent_local.py`.
- **Improve documentation** in `docs/`.

## Development setup

```bash
git clone https://github.com/<your-username>/SmartRecipe-AI.git
cd SmartRecipe-AI
pip install -r requirements.txt
python recipe_agent_local.py   # test the retrieval/scaling logic locally
```

## Pull request guidelines

1. Keep changes focused — one feature or fix per PR.
2. Test `recipe_agent_local.py` runs without errors after your change.
3. If you add a recipe, make sure the ingredient format matches existing rows
   so `scale_recipe.py` can parse it correctly.
4. Describe what you changed and why in the PR description.

## Scope

To keep this a lightweight, understandable student project, please avoid
adding: voice assistants, image recognition, mobile apps, authentication,
payments, additional databases, dashboards, multi-agent complexity, or
external APIs beyond IBM watsonx.ai. Larger feature ideas are welcome as
GitHub Issues for discussion first.

By contributing, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
