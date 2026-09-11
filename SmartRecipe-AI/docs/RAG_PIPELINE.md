# RAG Pipeline

SmartRecipe AI uses a lightweight Retrieval-Augmented Generation approach —
grounded generation without the overhead of embeddings or a vector
database, which keeps the project fast to build and cheap to run.

## Why RAG (and why a lightweight version)

Without retrieval, an LLM asked for "a recipe using rice, onion, and egg"
would generate something plausible but ungrounded — ingredient quantities,
steps, and timing might be inconsistent or unrealistic. By retrieving a real
recipe from a curated knowledge base first, the model has a concrete,
trustworthy reference to adapt, which reduces hallucination.

A full vector-database RAG pipeline (embeddings + similarity search) is
overkill for a knowledge base of a few dozen recipes. Instead, SmartRecipe
AI uses **tag/ingredient-overlap scoring**, which is transparent, fast, and
requires no additional infrastructure.

## Retrieval algorithm

Implemented in `recipe_agent_local.py` (`retrieve_best_recipe`):

1. **Parse** the user's ingredient list into a set of lowercase ingredient names.
2. **Score** every recipe in `data/recipes.csv` by counting how many of its
   required ingredients overlap with what the user has.
3. **Filter** out any recipe that doesn't match the user's stated dietary
   preference (via the `diet_tags` column).
4. **Rank** remaining candidates by overlap score, descending.
5. **Return** the top match.

```python
def score_recipe(row, user_ingredients, diet_pref):
    recipe_ingredients = {i.split(":")[0].strip().lower() for i in row["ingredients"].split(",")}
    overlap = len(user_ingredients & recipe_ingredients)
    if diet_pref and diet_pref.lower() not in [t.strip().lower() for t in row["diet_tags"].split(",")]:
        return -1  # disqualified
    return overlap
```

## Augmentation step

Before generation, the retrieved recipe is:

- **Scaled** to the user's requested serving size (`scale_recipe.py`)
- **Checked for missing ingredients** — anything in the recipe that the user
  didn't mention is flagged so the model can suggest a substitution instead
  of failing

## Generation step

The final prompt sent to the IBM Granite model combines:

1. `system_prompt.txt` — the persona and response-format instructions (sent
   once, as the system message)
2. The retrieved, scaled recipe + missing-ingredient note (sent as the user
   turn, built by `build_prompt()`)

This keeps the generation grounded in a real recipe while still letting the
model produce a natural, conversational response.

## Extending the knowledge base

To add more recipes, append rows to `data/recipes.csv` following the
existing column format. No re-indexing or embedding step is required —
retrieval works directly over the CSV.
