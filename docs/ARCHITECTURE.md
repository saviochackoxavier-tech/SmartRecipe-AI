# Architecture

## Overview

SmartRecipe AI is a single-flow Retrieval-Augmented Generation (RAG) agent.
There is deliberately **no multi-agent orchestration, no vector database,
and no external service beyond IBM watsonx.ai** — the whole system fits in
one Langflow canvas.

```
                 ┌─────────────────────────────────────────────┐
                 │           IBM Cloud Lite (hosting)           │
                 │                                               │
   User ───────▶ │  Langflow Chat Input                         │
                 │        │                                      │
                 │        ▼                                      │
                 │  Recipe Retrieval (RAG over recipes.csv)      │
                 │        │                                      │
                 │        ▼                                      │
                 │  Custom Component: scale_recipe.py            │
                 │  (adjusts ingredient quantities to servings)  │
                 │        │                                      │
                 │        ▼                                      │
                 │  Prompt Construction (Prompt Template)        │
                 │  = system_prompt.txt + retrieved recipe       │
                 │        │                                      │
                 │        ▼                                      │
                 │  IBM Granite model (via IBM watsonx.ai)        │
                 │        │                                      │
                 │        ▼                                      │
                 │  Langflow Chat Output ─────────────────▶ User │
                 └─────────────────────────────────────────────┘
```

## Components

| Component | Type | Responsibility |
|---|---|---|
| Chat Input | Langflow built-in | Captures the user's ingredients, dietary preference, and serving size |
| Recipe Retrieval | Langflow File/Loader + filter logic | Loads `data/recipes.csv` and finds the best-matching recipe (see `docs/RAG_PIPELINE.md`) |
| `scale_recipe.py` | Custom Python component | Scales ingredient quantities proportionally to the requested serving size |
| Prompt Template | Langflow built-in | Merges `system_prompt.txt` with the retrieved, scaled recipe into a single prompt |
| IBM Granite Model | IBM watsonx.ai Model component | Generates the final structured, natural-language recipe |
| Chat Output | Langflow built-in | Displays the response to the user |

## Design decisions

- **No vector database.** The knowledge base is small (a curated set of
  recipes), so a simple keyword/tag-overlap match is sufficient and avoids
  the cost/complexity of embeddings and a vector store.
- **No multi-agent framework.** A single flow with one model call keeps the
  project easy to understand, cheap to run, and easy to debug — appropriate
  for the project's scope.
- **Scaling as a separate, testable unit.** `scale_recipe.py` is a pure
  function with no side effects, which makes it easy to unit-test and easy
  to hand to an AI coding assistant (IBM Bob) for a quick, cheap review.

## Data flow example

1. User: *"I have rice, onion, egg — vegetarian, 3 servings."*
2. Retrieval matches **Tomato Onion Rice** (best ingredient overlap + diet tag match).
3. `scale_recipe.py` scales the recipe from its base 2 servings to 3.
4. The Prompt Template combines the persona instructions with the scaled
   recipe and any missing-ingredient note.
5. IBM Granite generates the final, friendly, structured recipe response.
6. Chat Output displays it to the user.
